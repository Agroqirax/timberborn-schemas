#!/usr/bin/env python3

# Validate all json files in a folder against json schema specified in catalog & print results
# Schema URIs pointing to this repo will be replaced with the local version of the same file
#
# Usage: python scripts/validate-all.py /path/to/folder
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
import re
from fnmatch import fnmatch
from jsonschema import Draft202012Validator

if len(sys.argv) != 2:
    print("[\033[31m✗\033[0m] Usage: python scripts/validate-all.py /path/to/folder")
    sys.exit(1)

folder = os.path.abspath(sys.argv[1])

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json5.load(f)

json_files = []
for root, _, files in os.walk(folder):
    for filename in files:
        if filename.lower().endswith(".blueprint.json"):
            json_files.append(os.path.join(root, filename))

RAW_RE = re.compile(
    r"https://raw\.githubusercontent\.com/agroqirax/timberborn-schemas/main/(.*)"
)

passed = 0
skipped = 0
failed = 0
total = len(json_files)

schema_cache = {}
validator_cache = {}

for json_file in json_files:
    rel_path = os.path.relpath(json_file, folder).replace("\\", "/")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json5.load(f)

    schema_url = None
    for entry in catalog.get("schemas", []):
        for pattern in entry.get("fileMatch", []):
            if fnmatch(rel_path, pattern.lstrip("./")):
                schema_url = entry["url"]
                break
        if schema_url:
            break

    if not schema_url:
        print(f"[\033[33m⚠\033[0m] No schema for file {rel_path}")
        skipped += 1
        continue

    m = RAW_RE.fullmatch(schema_url)
    if m:
        local_rel = m.group(1)
        schema_path = os.path.join(local_rel)
    else:
        schema_path = schema_url

    # Cache to prevent reloading large schemas many times
    if schema_path not in schema_cache:
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_cache[schema_path] = json5.load(f)
        except Exception as e:
            print(
                f"[\033[31m✗\033[0m] Could not load schema {schema_path}: {e}")
            skipped += 1
            continue

    schema = schema_cache[schema_path]

    if schema_path not in validator_cache:
        validator_cache[schema_path] = Draft202012Validator(schema)

    validator = validator_cache[schema_path]

    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))

    if not errors:
        print(f"[\033[32m✓\033[0m] {rel_path} passed")
        passed += 1
    else:
        print(f"[\033[31m✗\033[0m] {rel_path} failed")
        failed += 1
        for err in errors:
            loc = ".".join(map(str, err.path)) if err.path else "(root)"
            print(f"   \033[34m->\033[0m {loc}: {err.message}")

print(
    f"\n[\033[34m🛈\033[0m] Passed: {passed}/{total} ({round((passed/total) * 100, 1)}%)")
print(
    f"[\033[33m⚠\033[0m] Skipped: {skipped}/{total} ({round((skipped/total) * 100, 1)}%)")
print(
    f"[\033[31m✗\033[0m] Failed: {failed}/{total} ({round((failed/total) * 100, 1)}%)")
