# Developer Notes

These are here to help me remember how to do things.

## Setup Dev Environment

- `python3 -m pip install poetry`
- `poetry install`

## Update version

### Uses bump2version

- `bump2version patch --verbose --dry-run`

## Build

- `./build_readme.sh` to update the README.md uses Markdown Preprocessor
- `poetry build`

## Updating README.md

Do not directly edit README.md, instead edit README.mdpp and process with MarkdownPP using `build_readme.sh` to update README.md