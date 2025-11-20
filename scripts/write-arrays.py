#!/usr/bin/env python3

# Add #append, #remove & #delete postfix to all arrays
#
# Usage: python scripts/write-arrays.py /path/to/file.schema.json

import sys
import json5
import copy

if len(sys.argv) != 2:
    print("[\033[31m✗\033[0m] Usage: python scripts/write-arrays.py /path/to/file.schema.json")
    sys.exit(1)

schema_path = sys.argv[1]
with open(schema_path, "r", encoding="utf-8") as f:
    schema = json5.load(f)

if "$defs" not in schema:
    schema["$defs"] = {}

stack = [(schema, "root")]

while stack:
    node, path = stack.pop()
    if not isinstance(node, dict):
        continue

    props = node.get("properties")
    if isinstance(props, dict):
        for key, val in list(props.items()):
            if isinstance(val, dict) and val.get("type") == "array":
                if key not in schema["$defs"]:
                    schema["$defs"][key] = copy.deepcopy(val)

                props[f"{key}"] = {"$ref": f"#/$defs/{key}"}
                props[f"{key}#append"] = {"$ref": f"#/$defs/{key}"}
                props[f"{key}#remove"] = {"$ref": f"#/$defs/{key}"}

                props[f"{key}#delete"] = {"type": "object",
                                          "properties": {}, "additionalProperties": False}

            else:
                stack.append((val, f"{path}.properties.{key}"))

    for kw in ["items", "oneOf", "anyOf", "allOf"]:
        if kw in node:
            child = node[kw]
            if isinstance(child, dict):
                stack.append((child, f"{path}.{kw}"))
            elif isinstance(child, list):
                for i, item in enumerate(child):
                    if isinstance(item, dict):
                        stack.append((item, f"{path}.{kw}[{i}]"))

with open(schema_path, "w", encoding="utf-8") as f:
    json5.dump(schema, f, indent=2, quote_keys=True, trailing_commas=False)

print(
    f"[\033[32m✓\033[0m] (write-arrays) Updated schema written to {schema_path}")
