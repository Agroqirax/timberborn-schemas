This repo contains the json schemas for timberborn blueprints.

## Usage

The settings files for a few common editors are included in this repo. They will automatically load the correct schema for each file.

Copy your editors settings folder to your own project:

- Intellij IDEA: `./.idea/jsonSchemas.xml`
- Vscode: `./.vscode/settings.json`
- Zed: `./.zed/settings.json`

Visual studio 2022 does **not** currently support validating schemas with draft 2020-12

For other editors you may be able to import `catalog.json` or add the uri for each schema.<br>
The most common schemas and their uri's are listed below, a complete list can be found in `catalog.json`

## Schema list

- Asset meta specification (`/*.meta.json`) [wiki](https://github.com/mechanistry/timberborn-modding/wiki/Assets#images)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/asset.schema.json
  ```
- Building specification (`/Buildings/*/*/*.*.blueprint.json`)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/Building.schema.json
  ```
- Decal specification (`/Blueprints/Decals/Decal.*.*.blueprint.json`)

  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/Decal.schema.json
  ```

- Faction specification (`/Blueprints/Factions/Faction.*.blueprint.json`)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/Faction.schema.json
  ```
- Good specification (`/Blueprints/Goods/Good.*.blueprint.json`)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/Good.schema.json
  ```
- Mod manifest (`/manifest.json`)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/manifest.schema.json
  ```
- Need specification (`/Blueprints/Needs/Need.*.*.blueprint.json`)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/Need.schema.json
  ```
- Recipe specification (`/Blueprints/Recipes/Recipe.*.blueprint.json`)
  ```
  https://raw.githubusercontent.com/agroqirax/timberborn-schemas/main/schemas/Recipe.schema.json
  ```

## Contributing

The scripts folder contains a few helper scripts that aid the generation of json schemas.
The exact usage is explained in each file.

Vscode users can use tasks (`>Tasks: Run Task`) to automate running the scripts.
