#!/usr/bin/env python3

# Extract blueprints from assetripper export .asset files & save them as json files while preserving the directory structure
# 
# Usage: python scripts/fetch-exports.py /path/to/export
# 
# Use an environment:
# python -m venv .venv
# 
# Linux/macos: source ./.venv/bin/activate
# Windows: .\.venv\Scripts\activate
# 
# pip install -r requirements.txt

import os
import sys
import yaml
import json

class UnityYAMLLoader(yaml.SafeLoader):
    pass

def unknown_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return None

UnityYAMLLoader.add_multi_constructor('tag:unity3d.com,2011:', unknown_constructor)

if len(sys.argv) != 2:
    print("[\033[31m✗\033[0m] Usage: python scripts/fetch-exports.py /path/to/export")
    sys.exit(1)

base_path = os.path.abspath(sys.argv[1])
export_base = os.path.abspath("./exports/Data")

search_dirs = [
    os.path.join(base_path, "ExportedProject/Assets/Resources/blueprints"),
    os.path.join(base_path, "ExportedProject/Assets/Resources/buildings"),
]

for search_dir in search_dirs:
    if not os.path.isdir(search_dir):
        continue

    for root, _, files in os.walk(search_dir):
        for file in files:
            if not file.endswith(".blueprint.asset"):
                continue

            src_path = os.path.join(root, file)
            try:
                with open(src_path, "r", encoding="utf-8") as f:
                    yaml_data = yaml.load(f, Loader=UnityYAMLLoader)

                mono = yaml_data.get("MonoBehaviour", {})
                content = mono.get("_content", "")

                if not content:
                    print(f"[\033[33m⚠\033[0m] Skipped (no _content): {file}")
                    continue

                json_data = json.loads(content)

                if "Resources" in src_path:
                    rel_from_resources = src_path.split("Resources" + os.sep, 1)[1]
                else:
                    rel_from_resources = os.path.basename(src_path)

                json_rel_path = os.path.splitext(rel_from_resources)[0] + ".json"
                export_path = os.path.join(export_base, json_rel_path)

                os.makedirs(os.path.dirname(export_path), exist_ok=True)
                with open(export_path, "w", encoding="utf-8") as out:
                    json.dump(json_data, out, indent=2, ensure_ascii=False)

                print(f"[\033[32m✓\033[0m] Wrote: {file}")

            except Exception as e:
                print(f"[\033[31m✗\033[0m] {file}: {e}")

