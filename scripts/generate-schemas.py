#!/usr/bin/env python3

# Generate json schema from folder of example jsons
#
# Usage: python scripts/generate-schema.py /input/folder /output/file.schema.json
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
from genson import SchemaBuilder

if len(sys.argv) != 3:
    print("[\033[31m✗\033[0m] Usage: python scripts/generate-schema.py /input/folder /output/file.schema.json")
    sys.exit(1)

input_folder = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isdir(input_folder):
    print(
        f"[\033[31m✗\033[0m] Error: '{input_folder}' is not a valid directory.")
    sys.exit(1)

output_filename = os.path.basename(output_file)

merged_builder = SchemaBuilder()
merged_builder.add_schema({"type": "object"})

for root, _, files in os.walk(input_folder):
    for filename in files:
        if filename.lower().endswith(".json"):
            path = os.path.join(root, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json5.load(f)
                    file_builder = SchemaBuilder()
                    file_builder.add_schema({"type": "object"})
                    file_builder.add_object(data)
                    merged_builder.add_schema(file_builder.to_schema())
                print(f"[\033[32m✓\033[0m] Processed: {path}")
            except Exception as e:
                print(f"[\033[33m⚠\033[0m] Skipped {path}: {e}")

body_schema = merged_builder.to_schema()

body_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"

template = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": f"https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/{output_filename}",
    "title": "",
    "description": ""
}

template.update(body_schema)

with open(output_file, "w", encoding="utf-8") as f:
    json5.dump(template, f, indent=2, quote_keys=True, trailing_commas=False)

print(f"\n[\033[32m✓\033[0m] Merged schema saved to: {output_file}")
