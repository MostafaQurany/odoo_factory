#!/usr/bin/env python3
"""
scripts/factory/scan_modules.py

Automated AST-based Odoo module scanner.
Scans addons/ (vendor) and custom/ (project-owned), extracts manifests,
and writes .factory/generated/module_catalog.json and repository_catalog.json.
"""

import os
import sys
import ast
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def parse_manifest_ast(content: str) -> dict:
    """Safely parse an Odoo manifest string using AST literal evaluation."""
    try:
        tree = ast.parse(content)
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
                return ast.literal_eval(node.value)
    except Exception as e:
        # Fallback for expressions or complex manifests
        pass
    return {}

def scan_all_modules(project_root: Path = PROJECT_ROOT) -> tuple[dict, dict]:
    """
    Scans project_root/addons and project_root/custom.
    Returns (module_catalog, repository_catalog).
    """
    catalog = {}
    repos = {}

    vendor_dir = project_root / "addons"
    custom_dir = project_root / "custom"

    # 1. Scan vendor addons
    if vendor_dir.exists():
        for repo_path in sorted(vendor_dir.iterdir()):
            if repo_path.is_dir() and not repo_path.name.startswith("."):
                repo_name = repo_path.name
                repos[repo_name] = {
                    "name": repo_name,
                    "path": f"addons/{repo_name}",
                    "ownership": "vendor",
                    "modules": []
                }
                for module_path in sorted(repo_path.iterdir()):
                    manifest_file = module_path / "__manifest__.py"
                    if module_path.is_dir() and manifest_file.exists():
                        tech_name = module_path.name
                        repos[repo_name]["modules"].append(tech_name)
                        try:
                            content = manifest_file.read_text(encoding="utf-8", errors="replace")
                            manifest = parse_manifest_ast(content)
                        except Exception:
                            manifest = {}

                        catalog[tech_name] = {
                            "technical_name": tech_name,
                            "display_name": manifest.get("name", tech_name),
                            "repository": repo_name,
                            "path": f"addons/{repo_name}/{tech_name}",
                            "version": str(manifest.get("version", "18.0.1.0.0")),
                            "license": manifest.get("license", "LGPL-3"),
                            "category": manifest.get("category", "Uncategorized"),
                            "summary": manifest.get("summary", ""),
                            "depends": manifest.get("depends", []),
                            "auto_install": manifest.get("auto_install", False),
                            "installable": manifest.get("installable", True),
                            "application": manifest.get("application", False),
                            "external_dependencies": manifest.get("external_dependencies", {}),
                            "ownership": "vendor",
                            "classification": "UNCLASSIFIED",
                            "capabilities": [],
                            "odoo_version": "18.0",
                            "edition_requirement": "community",
                            "status": "active",
                            "risk": "low"
                        }

    # 2. Scan custom addons
    if custom_dir.exists():
        for module_path in sorted(custom_dir.iterdir()):
            manifest_file = module_path / "__manifest__.py"
            if module_path.is_dir() and manifest_file.exists():
                tech_name = module_path.name
                try:
                    content = manifest_file.read_text(encoding="utf-8", errors="replace")
                    manifest = parse_manifest_ast(content)
                except Exception:
                    manifest = {}

                catalog[tech_name] = {
                    "technical_name": tech_name,
                    "display_name": manifest.get("name", tech_name),
                    "repository": "custom",
                    "path": f"custom/{tech_name}",
                    "version": str(manifest.get("version", "18.0.1.0.0")),
                    "license": manifest.get("license", "LGPL-3"),
                    "category": manifest.get("category", "Custom"),
                    "summary": manifest.get("summary", ""),
                    "depends": manifest.get("depends", []),
                    "auto_install": manifest.get("auto_install", False),
                    "installable": manifest.get("installable", True),
                    "application": manifest.get("application", False),
                    "external_dependencies": manifest.get("external_dependencies", {}),
                    "ownership": "custom",
                    "classification": "UNCLASSIFIED",
                    "capabilities": [],
                    "odoo_version": "18.0",
                    "edition_requirement": "community",
                    "status": "active",
                    "risk": "low"
                }

    return catalog, repos

def main():
    print(f"[*] Scanning modules in {PROJECT_ROOT}...")
    catalog, repos = scan_all_modules(PROJECT_ROOT)
    print(f"[+] Discovered {len(catalog)} total modules across {len(repos)} repositories and custom/ directory.")

    output_dir = PROJECT_ROOT / ".factory" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    catalog_file = output_dir / "module_catalog.json"
    repo_file = output_dir / "repository_catalog.json"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"[+] Written module catalog to {catalog_file}")

    with open(repo_file, "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)
    print(f"[+] Written repository catalog to {repo_file}")

if __name__ == "__main__":
    main()
