#!/usr/bin/env python3

# Generate editor settings files (vsc, zed, idea) based on catalog.json
# 
# Usage: python scripts/generate-settings.py

import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Input and output paths
CATALOG_PATH = "./catalog.json"
VSCODE_PATH = "./.vscode/settings.json"
ZED_PATH = "./.zed/settings.json"
IDEA_PATH = "./.idea/jsonSchemas.xml"

os.makedirs(os.path.dirname(VSCODE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(ZED_PATH), exist_ok=True)
os.makedirs(os.path.dirname(IDEA_PATH), exist_ok=True)

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

schemas = catalog.get("schemas", [])

# Vscode
vscode_config = {
    "json.schemas": [
        {"fileMatch": s["fileMatch"], "url": s["url"]}
        for s in schemas
    ]
}
with open(VSCODE_PATH, "w", encoding="utf-8") as f:
    json.dump(vscode_config, f, indent=2)
print(f"[\033[32m✓\033[0m] Wrote VS Code settings to {VSCODE_PATH}")

# Zed
zed_config = {
    "lsp": {
        "json-language-server": {
            "settings": {
                "json": {
                    "schemas": [
                        {"fileMatch": s["fileMatch"], "url": s["url"]}
                        for s in schemas
                    ]
                }
            }
        }
    }
}
with open(ZED_PATH, "w", encoding="utf-8") as f:
    json.dump(zed_config, f, indent=2)
print(f"[\033[32m✓\033[0m] Wrote Zed settings to {ZED_PATH}")

# Idea
project = Element("project", version="4")
component = SubElement(project, "component", name="JsonSchemaMappingsProjectConfiguration")
state = SubElement(component, "state")
map_el = SubElement(state, "map")

for s in schemas:
    entry = SubElement(map_el, "entry", key=s["name"])
    value = SubElement(entry, "value")
    schema_info = SubElement(value, "SchemaInfo")

    SubElement(schema_info, "option", name="generatedName", value="New Schema")
    SubElement(schema_info, "option", name="name", value=s["name"])
    SubElement(schema_info, "option", name="relativePathToSchema", value=s["url"])

    patterns_option = SubElement(schema_info, "option", name="patterns")
    list_el = SubElement(patterns_option, "list")
    for pattern in s["fileMatch"]:
        item = SubElement(list_el, "Item")
        SubElement(item, "option", name="path", value=pattern)

xml_str = minidom.parseString(tostring(project, encoding="utf-8")).toprettyxml(indent="  ", encoding="UTF-8")

with open(IDEA_PATH, "wb",) as f:
    f.write(xml_str)

print(f"[\033[32m✓\033[0m] Wrote IntelliJ IDEA settings to {IDEA_PATH}")
