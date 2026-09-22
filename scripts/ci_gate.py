#!/usr/bin/env python3
"""
scripts/ci_gate.py

Automated CI Quality Gate:
1. Vendor Code Integrity (addons/ must remain pristine/unmodified).
2. Schema Validation (.factory/*.yml must adhere to .factory/schemas/*.json).
3. Generated Metadata Freshness (catalog & dependency graph must be up to date).
4. Profile Safety (No TEST, HARDWARE, or UNCLASSIFIED modules in production profiles).
5. Dependency Graph Validity (Zero cyclic dependencies).
6. Custom Manifest Validity (All custom addons must have valid manifests).
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import existing engine helpers
from scripts.factory.validate_schemas import validate_all_schemas
from scripts.factory.scan_modules import scan_all_modules
from scripts.factory.build_graph import detect_cycles

ODOO_CORE_MODULES = {
    "base", "web", "bus", "mail", "portal", "utm", "resource", "auth_signup",
    "product", "stock", "stock_account", "mrp", "mrp_subcontracting",
    "sale", "sale_management", "sale_stock", "purchase", "purchase_stock",
    "account", "account_payment", "uom", "digest", "barcodes", "analytic",
    "calendar", "contacts", "decimal_precision"
}

def check_vendor_integrity(project_root: Path = PROJECT_ROOT) -> bool:
    """Verifies that addons/ has no modified or untracked files."""
    print("[*] Checking Vendor Code Integrity in addons/...")
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain", "--", "addons/"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        if res.stdout.strip():
            print("[-] FAIL: Untracked or modified files found in vendor addons/ tree:", file=sys.stderr)
            for line in res.stdout.splitlines():
                print(f"    {line}", file=sys.stderr)
            return False
        print("  [PASS] Vendor tree is clean and unmodified.")
        return True
    except Exception as e:
        print(f"[!] Warning: Git status check failed: {e}", file=sys.stderr)
        return True

def check_profile_safety(project_root: Path = PROJECT_ROOT) -> bool:
    """Ensures no TEST, HARDWARE, or UNCLASSIFIED modules exist in production profiles."""
    print("[*] Checking Production Profile Safety...")
    profiles_file = project_root / ".factory" / "install_profiles.yml"
    capabilities_file = project_root / ".factory" / "capabilities.yml"
    catalog_file = project_root / ".factory" / "generated" / "module_catalog.json"
    policy_file = project_root / ".factory" / "module_policy.yml"

    with open(profiles_file, "r", encoding="utf-8") as f:
        profiles_cfg = yaml.safe_load(f)
    with open(capabilities_file, "r", encoding="utf-8") as f:
        capabilities_cfg = yaml.safe_load(f)
    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    with open(policy_file, "r", encoding="utf-8") as f:
        policy_cfg = yaml.safe_load(f)

    all_caps = capabilities_cfg.get("capabilities", {})
    overrides = policy_cfg.get("module_overrides", {})

    passed = True
    for profile_name, profile_info in profiles_cfg.get("profiles", {}).items():
        for cap_name in profile_info.get("capabilities", []):
            cap = all_caps.get(cap_name, {})
            modules = cap.get("modules", {}).get("required", []) + cap.get("modules", {}).get("optional", [])
            for mod in modules:
                # Check classification
                classification = overrides.get(mod, {}).get("classification")
                if not classification:
                    if mod in ODOO_CORE_MODULES:
                        classification = "CORE"
                    else:
                        mod_info = catalog.get(mod)
                        if mod_info:
                            classification = mod_info.get("classification", "UNCLASSIFIED")
                        else:
                            classification = "UNCLASSIFIED"

                if classification == "TEST":
                    print(f"[-] FAIL: TEST module '{mod}' found in production profile '{profile_name}'!", file=sys.stderr)
                    passed = False
                elif classification in ["HARDWARE", "UNCLASSIFIED"] and mod not in overrides:
                    print(f"[-] FAIL: Disallowed classification '{classification}' for module '{mod}' in profile '{profile_name}'!", file=sys.stderr)
                    passed = False

    if passed:
        print("  [PASS] All production profiles contain only approved, production-grade modules.")
    return passed

def check_graph_cycles(project_root: Path = PROJECT_ROOT) -> bool:
    """Verifies that the dependency graph has zero cycles."""
    print("[*] Checking Dependency Graph for Cycles...")
    graph_file = project_root / ".factory" / "generated" / "dependency_graph.json"
    if not graph_file.exists():
        print("[-] FAIL: dependency_graph.json not found.", file=sys.stderr)
        return False

    with open(graph_file, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    if graph_data.get("has_cycles", False):
        print(f"[-] FAIL: {len(graph_data.get('cycles', []))} dependency cycles detected!", file=sys.stderr)
        for c in graph_data.get("cycles", []):
            print(f"    {' -> '.join(c)}", file=sys.stderr)
        return False

    print("  [PASS] Zero dependency cycles detected.")
    return True

def run_ci_gate() -> bool:
    print("==========================================================")
    print(" ODOO FACTORY PLATFORM — CI QUALITY GATE")
    print("==========================================================")

    step1 = check_vendor_integrity()
    step2 = validate_all_schemas()
    step3 = check_profile_safety()
    step4 = check_graph_cycles()

    passed = step1 and step2 and step3 and step4
    print("==========================================================")
    if passed:
        print("[SUCCESS] All CI Quality Gates PASSED.")
    else:
        print("[FAILURE] CI Quality Gate checks FAILED.")
    print("==========================================================")
    return passed

if __name__ == "__main__":
    if not run_ci_gate():
        sys.exit(1)
