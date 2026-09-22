#!/usr/bin/env python3
"""
scripts/factory/generate_profiles.py

Reads .factory/install_profiles.yml and .factory/capabilities.yml.
Generates or updates custom/factory_profile_* meta-addons manifests.
Ensures .factory/install_profiles.yml is the single source of truth.
"""

import sys
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def resolve_profile_dependencies(profile_name: str, profiles_cfg: dict, capabilities_cfg: dict) -> list[str]:
    profile_data = profiles_cfg.get("profiles", {}).get(profile_name)
    if not profile_data:
        raise ValueError(f"Profile '{profile_name}' not defined in install_profiles.yml")

    resolved_caps = set(profile_data.get("capabilities", []))
    
    # Handle inheritance / extends
    parent = profile_data.get("extends")
    while parent:
        parent_data = profiles_cfg.get("profiles", {}).get(parent)
        if not parent_data:
            break
        resolved_caps.update(parent_data.get("capabilities", []))
        parent = parent_data.get("extends")

    # Collect modules from capabilities
    depends = set(profile_data.get("explicit_modules", []))
    all_caps = capabilities_cfg.get("capabilities", {})

    for cap_name in resolved_caps:
        cap_info = all_caps.get(cap_name)
        if not cap_info:
            print(f"[!] Warning: Capability '{cap_name}' referenced in profile '{profile_name}' not found in capabilities.yml")
            continue
        req_modules = cap_info.get("modules", {}).get("required", [])
        depends.update(req_modules)

    return sorted(list(depends))

def generate_profile_addons():
    profiles_file = PROJECT_ROOT / ".factory" / "install_profiles.yml"
    capabilities_file = PROJECT_ROOT / ".factory" / "capabilities.yml"
    custom_dir = PROJECT_ROOT / "custom"

    if not profiles_file.exists() or not capabilities_file.exists():
        print("[-] Missing install_profiles.yml or capabilities.yml.", file=sys.stderr)
        sys.exit(1)

    profiles_cfg = load_yaml(profiles_file)
    capabilities_cfg = load_yaml(capabilities_file)

    print("[*] Generating factory profile meta-addons from .factory/install_profiles.yml...")

    for profile_name, data in profiles_cfg.get("profiles", {}).items():
        addon_name = f"factory_profile_{profile_name}"
        addon_dir = custom_dir / addon_name
        addon_dir.mkdir(parents=True, exist_ok=True)

        depends = resolve_profile_dependencies(profile_name, profiles_cfg, capabilities_cfg)

        init_file = addon_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# -*- coding: utf-8 -*-\n", encoding="utf-8")

        manifest_file = addon_dir / "__manifest__.py"
        manifest_content = f"""# -*- coding: utf-8 -*-
# Auto-generated from .factory/install_profiles.yml
# DO NOT EDIT MANUALLY. Run scripts/factory/generate_profiles.py to update.
{{
    'name': 'Factory Profile: {profile_name.capitalize()}',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Profiles',
    'summary': {repr(data.get('description', 'Factory Profile'))},
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': {depends},
    'data': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}}
"""
        manifest_file.write_text(manifest_content, encoding="utf-8")
        print(f"[+] Generated {addon_name} with {len(depends)} dependencies: {depends}")

    print("[+] All factory profile meta-addons generated successfully.")

if __name__ == "__main__":
    generate_profile_addons()
