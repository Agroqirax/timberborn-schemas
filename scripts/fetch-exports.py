#!/usr/bin/env python3

# Extract blueprints from assetripper export .asset files & save them as json files while preserving the directory structure
# Obsolete. Use Timberborn_Data/StreamingAssets/Modding/Blueprints.zip from the timberborn install location
#
# Usage: python scripts/fetch-exports.py /path/to/export /path/to/output
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


UnityYAMLLoader.add_multi_constructor(
    'tag:unity3d.com,2011:', unknown_constructor)

if len(sys.argv) != 3:
    print("[\033[31m✗\033[0m] Usage: python scripts/fetch-exports.py /path/to/export /path/to/output")
    sys.exit(1)

input_base, output_base = sys.argv[1], sys.argv[2]

for root, _, files in os.walk(input_base):
    for file in files:
        if not file.endswith(".blueprint.asset"):
            continue

        src_path = os.path.join(root, file)

        with open(src_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f, Loader=UnityYAMLLoader)

        mono = yaml_data.get("MonoBehaviour", {})
        content = mono.get("_content", "")

        json_data = json.loads(content)

        if "Resources" in src_path:
            rel_from_resources = src_path.split("Resources" + os.sep, 1)[1]
        else:
            rel_from_resources = os.path.basename(src_path)

        json_rel_path = os.path.splitext(rel_from_resources)[0] + ".json"
        export_path = os.path.join(output_base, json_rel_path)

        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        with open(export_path, "w", encoding="utf-8") as out:
            json.dump(json_data, out, indent=2, ensure_ascii=False)

        print(f"[\033[32m✓\033[0m] Wrote: {file}")
