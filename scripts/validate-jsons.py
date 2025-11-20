#!/usr/bin/env python3

# Validate all json files in a folder against a json schema & print results
#
# Usage: python scripts/validate-jsons.py /path/to/file.schema.json /path/to/folder
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
import json5
from jsonschema import validators

if len(sys.argv) != 3:
    print("[\033[31m✗\033[0m] Usage: python scripts/validate-jsons.py /path/to/file.schema.json /path/to/folder")
    sys.exit(1)

schema_path, json_folder = sys.argv[1], sys.argv[2]

with open(schema_path, 'r', encoding='utf-8') as f:
    schema = json5.load(f)


ValidatorClass = validators.validator_for(schema)
ValidatorClass.check_schema(schema)
validator = ValidatorClass(schema)

json_files = []
for root, dirs, files in os.walk(json_folder):
    for filename in files:
        if filename.lower().endswith(".json"):
            json_files.append(os.path.join(root, filename))

passed = 0
failed = 0
total = len(json_files)
for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json5.load(f)

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if not errors:
        print(f"[\033[32m✓\033[0m] File {json_file} passed")
        passed += 1
    else:
        print(f"[\033[31m✗\033[0m] File {json_file} failed")
        for err in errors:
            location = ".".join(map(str, err.path)) if err.path else "(root)"
            print(f"   \033[34m->\033[0m {location} {err.message}")

print(
    f"\n[\033[34m🛈\033[0m] Passed: {passed}/{total} ({round(passed/total*100, 1)}%)")
print(
    f"[\033[31m✗\033[0m] Failed: {failed}/{total} ({round((failed/total) * 100, 1)}%)")
