#!/usr/bin/env python3
"""
scripts/factory/build_graph.py

Constructs directed dependency graph from module catalog, detects cycles,
identifies missing dependencies, and outputs .factory/generated/dependency_graph.json.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Core built-in Odoo addons that might not be in our vendor/custom directories
ODOO_CORE_ADDONS = {
    "base", "web", "bus", "mail", "portal", "utm", "resource", "auth_signup",
    "product", "stock", "stock_account", "mrp", "mrp_subcontracting",
    "sale", "sale_management", "sale_stock", "purchase", "purchase_stock",
    "account", "account_payment", "uom", "digest", "barcodes", "analytic",
    "calendar", "contacts", "decimal_precision", "fetchmail", "gamification",
    "http_routing", "iap", "link_tracker", "payment", "phone_validation",
    "privacy_lookup", "rating", "snailmail", "survey", "web_editor",
    "web_tour", "web_unsplash"
}

def detect_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    """
    Detects all cycles in a directed graph using DFS.
    Returns list of cycle paths.
    """
    cycles = []
    visited: Set[str] = set()
    rec_stack: List[str] = []

    def dfs(node: str):
        visited.add(node)
        rec_stack.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                cycle_start_idx = rec_stack.index(neighbor)
                cycle = rec_stack[cycle_start_idx:] + [neighbor]
                cycles.append(cycle)

        rec_stack.pop()

    for n in list(graph.keys()):
        if n not in visited:
            dfs(n)

    return cycles

def build_dependency_graph(catalog: dict) -> dict:
    """
    Builds the dependency graph, identifies missing dependencies,
    and runs cycle detection.
    """
    graph: Dict[str, List[str]] = {}
    missing_deps: Dict[str, List[str]] = {}
    available_modules = set(catalog.keys()).union(ODOO_CORE_ADDONS)

    for tech_name, info in catalog.items():
        deps = info.get("depends", [])
        graph[tech_name] = deps
        missing = [d for d in deps if d not in available_modules]
        if missing:
            missing_deps[tech_name] = missing

    cycles = detect_cycles(graph)

    return {
        "nodes": list(catalog.keys()),
        "edges": graph,
        "cycles": cycles,
        "has_cycles": len(cycles) > 0,
        "missing_dependencies": missing_deps,
        "total_modules": len(catalog),
        "total_edges": sum(len(d) for d in graph.values())
    }

def main():
    catalog_path = PROJECT_ROOT / ".factory" / "generated" / "module_catalog.json"
    if not catalog_path.exists():
        print(f"[-] Catalog not found at {catalog_path}. Please run scan_modules.py first.", file=sys.stderr)
        sys.exit(1)

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"[*] Building dependency graph for {len(catalog)} modules...")
    result = build_dependency_graph(catalog)

    output_path = PROJECT_ROOT / ".factory" / "generated" / "dependency_graph.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[+] Dependency graph written to {output_path}")
    print(f"    Total modules : {result['total_modules']}")
    print(f"    Total edges   : {result['total_edges']}")
    print(f"    Cycles detected: {len(result['cycles'])}")

    if result['has_cycles']:
        print(f"[!] WARNING: Cyclic dependencies detected:")
        for c in result['cycles']:
            print(f"    {' -> '.join(c)}")
    else:
        print("[+] Dependency graph is valid (no cycles detected).")

    if result['missing_dependencies']:
        print(f"[*] Note: {len(result['missing_dependencies'])} modules reference upstream/unscanned dependencies.")

if __name__ == "__main__":
    main()
