#!/usr/bin/env python3

# Find & replace common issues
# 
# Usage: python scripts/write-replace.py /path/to/file.schema.json

import sys
import re

if len(sys.argv) != 2:
    print("[\033[31m✗\033[0m] Usage: python scripts/write-replace.py /path/to/file.schema.json")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    (r'"title": "(.*)spec"', r'"title": "\1specification"'), # Change spec to specification in titles
    (r'"required": \[.*?\]', r'"minProperties":1,"additionalProperties":false'), # Remove required arrays & add replacement restrictions
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[\033[32m✓\033[0m] Updated schema written to {filename}")
