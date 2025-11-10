#!/usr/bin/env python3

# Write titles to json schema based on key name
# 
# Usage: python scripts/write-titles.py /path/to/file.schema.json

import json
import sys
import re

if len(sys.argv) != 2:
    print(f"[\033[31m✗\033[0m] Usage: python scripts/write-titles.py /path/to/file.schema.json")
    sys.exit(1)

schema_path = sys.argv[1]

with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

stack = [schema]

while stack:
    current = stack.pop()

    if not isinstance(current, dict):
        continue
    if "items" in current and isinstance(current["items"], dict):
        stack.append(current["items"])

    props = current.get("properties")
    if props and isinstance(props, dict):
        for key, value in props.items():
            if isinstance(value, dict):
                if "title" not in value:
                    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', key)
                    title = spaced.capitalize()
                    value["title"] = title
                stack.append(value)

with open(schema_path, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2)

print(f"[\033[32m✓\033[0m] Updated schema written to {schema_path}")
