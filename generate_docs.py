import os
import ast
from collections import defaultdict

def parse_manifest(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Odoo manifests are python dictionaries.
            manifest = ast.literal_eval(content)
            return manifest
    except Exception as e:
        print(f"Warning: Could not parse {filepath} due to {e}")
        return {}

def generate_documentation(addons_path, output_file):
    # Dictionary to hold addons categorized by their parent folder
    # Example: categorized_addons['web'] = [{manifest_dict}, ...]
    categorized_addons = defaultdict(list)
    
    for root, dirs, files in os.walk(addons_path):
        if '__manifest__.py' in files:
            manifest_path = os.path.join(root, '__manifest__.py')
            manifest = parse_manifest(manifest_path)
            
            if manifest:
                # Find the immediate subdirectory under 'addons'
                rel_path = os.path.relpath(root, addons_path)
                category_folder = rel_path.split(os.sep)[0]
                
                # Add folder name to manifest for reference
                manifest['_folder'] = os.path.basename(root)
                categorized_addons[category_folder].append(manifest)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Odoo Addons Documentation\n\n")
        f.write("This document provides a comprehensive overview of all modules located in the `addons` directory.\n\n")
        
        for category, addons in sorted(categorized_addons.items()):
            f.write(f"## {category.title().replace('-', ' ')}\n\n")
            
            # Sort addons by name for better readability
            addons.sort(key=lambda x: x.get('name', x.get('_folder', '')))
            
            for addon in addons:
                name = addon.get('name', addon.get('_folder', 'Unknown'))
                version = addon.get('version', 'N/A')
                summary = addon.get('summary', 'No summary provided.')
                author = addon.get('author', 'Unknown')
                depends = addon.get('depends', [])
                
                f.write(f"### {name}\n")
                f.write(f"- **Technical Name**: `{addon.get('_folder')}`\n")
                f.write(f"- **Version**: {version}\n")
                f.write(f"- **Author**: {author}\n")
                if depends:
                    f.write(f"- **Dependencies**: `{', '.join(depends)}`\n")
                f.write(f"- **Summary**: {summary}\n\n")
                
                description = addon.get('description', '')
                if description:
                    f.write(f"**Description**:\n")
                    # Keep description indented if it has multiple lines
                    for line in description.splitlines():
                        f.write(f"> {line}\n")
                    f.write("\n")
                
                f.write("---\n\n")

if __name__ == "__main__":
    addons_dir = r"e:\C\production projects\amgad\odoo_factory\addons"
    out_file = r"C:\Users\qmost\.gemini\antigravity-ide\brain\2bdb6cb3-da2f-456c-9e17-7880204b3231\addons_documentation.md"
    generate_documentation(addons_dir, out_file)
    print(f"Documentation generated successfully at: {out_file}")
