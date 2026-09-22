#!/usr/bin/env python3
"""
scripts/factory/validate_schemas.py

Validates all declarative YAML contracts in .factory/
against their corresponding JSON schemas in .factory/schemas/.
"""

import sys
import json
import yaml
from pathlib import Path
import jsonschema

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

SCHEMA_MAP = {
    "project.yml": "project.schema.json",
    "capabilities.yml": "capabilities.schema.json",
    "module_policy.yml": "module_policy.schema.json",
    "install_profiles.yml": "install_profiles.schema.json",
    "golden_scenario.yml": "golden_scenario.schema.json",
    "health_checks.yml": "health_checks.schema.json",
}

def validate_all_schemas(project_root: Path = PROJECT_ROOT) -> bool:
    factory_dir = project_root / ".factory"
    schemas_dir = factory_dir / "schemas"

    all_passed = True
    print(f"[*] Validating YAML contracts in {factory_dir} against schemas in {schemas_dir}...")

    for yaml_name, schema_name in SCHEMA_MAP.items():
        yaml_file = factory_dir / yaml_name
        schema_file = schemas_dir / schema_name

        if not yaml_file.exists():
            print(f"[-] ERROR: Missing YAML contract: {yaml_file}", file=sys.stderr)
            all_passed = False
            continue

        if not schema_file.exists():
            print(f"[-] ERROR: Missing Schema definition: {schema_file}", file=sys.stderr)
            all_passed = False
            continue

        try:
            with open(yaml_file, "r", encoding="utf-8") as yf:
                data = yaml.safe_load(yf)
        except Exception as e:
            print(f"[-] ERROR parsing YAML in {yaml_file}: {e}", file=sys.stderr)
            all_passed = False
            continue

        try:
            with open(schema_file, "r", encoding="utf-8") as sf:
                schema = json.load(sf)
        except Exception as e:
            print(f"[-] ERROR parsing Schema in {schema_file}: {e}", file=sys.stderr)
            all_passed = False
            continue

        try:
            jsonschema.validate(instance=data, schema=schema)
            print(f"  [PASS] {yaml_name} adheres to {schema_name}")
        except jsonschema.ValidationError as err:
            print(f"  [FAIL] {yaml_name} fails validation against {schema_name}:", file=sys.stderr)
            print(f"         {err.message}", file=sys.stderr)
            all_passed = False

    return all_passed

def main():
    success = validate_all_schemas()
    if success:
        print("[+] All declarative contracts are valid and compliant with schemas.")
        sys.exit(0)
    else:
        print("[-] Schema validation failed.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
