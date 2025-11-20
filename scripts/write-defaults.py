#!/usr/bin/env python3

# Write default and example values to schema based on folder of example json files
#
# Usage: python scripts/write-defaults.py /path/to/file.schema.json /path/to/folder

import sys
import json5
import os
from collections import Counter

if len(sys.argv) != 3:
    print("[\033[31m✗\033[0m] Usage: python scripts/write-defaults.py path/to/file.schema.json /path/to/folder")
    sys.exit(1)

schema_path = sys.argv[1]
folder = sys.argv[2]

with open(schema_path, "r", encoding="utf-8") as f:
    schema = json5.load(f)

props = []

stack = [(schema, [])]

while stack:
    node, path = stack.pop()
    if isinstance(node, dict):
        if node.get("type") == "object" and "properties" in node:
            for k, v in node["properties"].items():
                stack.append((v, path + [("properties", k)]))
        elif node.get("type") == "array" and "items" in node:
            stack.append((node["items"], path + [("items",)]))

        t = node.get("type")
        if t in ("string", "number", "boolean"):
            props.append((schema, path, node))

json_files = []
for root, _, files in os.walk(folder):
    for file in files:
        if file.lower().endswith(".json"):
            json_files.append(os.path.join(root, file))


def get_value(data, path):
    try:
        for step in path:
            if step[0] == "properties":
                data = data.get(step[1], None)
            elif step[0] == "items":
                if isinstance(data, list):
                    data = data
                else:
                    return []
        if isinstance(data, list):
            return data
        return [data]
    except:
        return []


values_map = {}
for (_, path, _) in props:
    values_map[tuple(path)] = []

for jf in json_files:
    try:
        with open(jf, "r", encoding="utf-8") as f:
            data = json5.load(f)
    except:
        continue

    for (_, path, _) in props:
        vals = get_value(data, path)
        for v in vals:
            if isinstance(v, (str, int, float, bool)):
                values_map[tuple(path)].append(v)

for (root_schema, path, node) in props:
    vals = values_map.get(tuple(path), [])
    if not vals:
        continue

    counts = Counter(vals)
    most_common = counts.most_common()

    ex = [v for v, c in most_common]
    node["examples"] = ex

    if len(most_common) == 1 or (len(most_common) > 1 and most_common[0][1] > most_common[1][1]):
        node["default"] = most_common[0][0]

with open(schema_path, "w", encoding="utf-8") as f:
    json5.dump(schema, f, indent=2, quote_keys=True, trailing_commas=False)

print(
    f"[\033[32m✓\033[0m] (write-defaults) Updated schema written to {schema_path}")
