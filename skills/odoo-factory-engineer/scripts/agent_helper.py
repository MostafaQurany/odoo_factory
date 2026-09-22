#!/usr/bin/env python3
"""
skills/odoo-factory-engineer/scripts/agent_helper.py

Agent CLI assistant for inspecting Odoo Factory Platform contracts,
querying module catalog, capability mapping, and impact analysis.
"""

import sys
import json
import yaml
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

def load_catalog():
    path = PROJECT_ROOT / ".factory" / "generated" / "module_catalog.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_capabilities():
    path = PROJECT_ROOT / ".factory" / "capabilities.yml"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("capabilities", {})

def load_scenarios():
    path = PROJECT_ROOT / ".factory" / "golden_scenario.yml"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def inspect_module(mod_name, catalog):
    info = catalog.get(mod_name)
    if not info:
        print(f"[-] Module '{mod_name}' not found in catalog.")
        return
    print(f"=== Module: {mod_name} ===")
    print(f"  Display Name : {info.get('display_name')}")
    print(f"  Repository   : {info.get('repository')} ({info.get('ownership')})")
    print(f"  Path         : {info.get('path')}")
    print(f"  License      : {info.get('license')}")
    print(f"  Dependencies : {', '.join(info.get('depends', []))}")
    print(f"  Classification: {info.get('classification')}")
    if info.get("ownership") == "vendor":
        print("  [!] RULE: Vendor module. READ-ONLY. Do not edit directly.")

def inspect_capability(cap_name, capabilities):
    for key, info in capabilities.items():
        if cap_name.lower() in key.lower():
            print(f"=== Capability: {key} ===")
            print(f"  Status       : {info.get('status')}")
            print(f"  Classification: {info.get('classification')}")
            print(f"  Description  : {info.get('description')}")
            print(f"  Requires     : {', '.join(info.get('requires', []))}")
            print(f"  Modules (Req): {', '.join(info.get('modules', {}).get('required', []))}")
            print(f"  Modules (Opt): {', '.join(info.get('modules', {}).get('optional', []))}")
            print(f"  Impact Tests : {', '.join(info.get('tests', []))}")
            return
    print(f"[-] Capability matching '{cap_name}' not found.")

def inspect_impact(mod_name, scenarios):
    impacted = []
    for code, sc in scenarios.get("scenarios", {}).items():
        if mod_name in sc.get("modules", []):
            impacted.append((code, sc.get("title")))
    for code, sc in scenarios.get("cross_cutting", {}).items():
        if mod_name in sc.get("modules", []):
            impacted.append((code, sc.get("title")))

    print(f"=== Impact Analysis for: {mod_name} ===")
    if not impacted:
        print("  No direct Golden Scenario mappings found.")
    else:
        print(f"  Trigger following scenarios after changes to '{mod_name}':")
        for code, title in impacted:
            print(f"    - [{code}] {title}")

def main():
    parser = argparse.ArgumentParser(description="Odoo Factory Agent Helper")
    parser.add_argument("--module", "-m", help="Inspect module metadata and ownership")
    parser.add_argument("--capability", "-c", help="Inspect business capability mapping")
    parser.add_argument("--impact", "-i", help="Run impact analysis for modified module")

    args = parser.parse_args()
    catalog = load_catalog()
    capabilities = load_capabilities()
    scenarios = load_scenarios()

    if args.module:
        inspect_module(args.module, catalog)
    elif args.capability:
        inspect_capability(args.capability, capabilities)
    elif args.impact:
        inspect_impact(args.impact, scenarios)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
