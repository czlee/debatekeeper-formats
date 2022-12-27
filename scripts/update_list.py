#!/usr/bin/env python
"""Updates the list in formats.json. Should be run after any updates to formats, and the result
committed to the repository."""

import argparse
import json
from pathlib import Path

from lxml import etree

from validate_xml_schema import validate_xml_schema

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("formats_dir", nargs="?", default=Path("v1/formats"), type=Path)
parser.add_argument("-O", "--output-file", default="v1/formats.json")
parser.add_argument("--add-errors", action="store_true",
    help="Adds some erroneous entries to test error conditions in the app")
args = parser.parse_args()

if not args.formats_dir.is_dir():
    print(f"{args.formats_dir} is not a directory")
    exit(1)

formats = []

LANG_ATTR = "{http://www.w3.org/XML/1998/namespace}lang"

for path in args.formats_dir.iterdir():
    if path.suffix != ".xml":
        print(f"skipping {path}")
        continue

    errors = validate_xml_schema(path)
    if errors:
        print("\n".join(errors))

    root = etree.parse(open(path))

    # respect order of declared languages if there are any...
    infos = {e.text: {} for e in root.findall("./languages/language")}

    for e in root.findall("name"):
        # ...but declared languages aren't always mandatory, so fall back to name order
        infos.setdefault(e.get(LANG_ATTR, ""), {}).update({"name": e.text})

    for info in root.findall("info"):
        infos[info.get(LANG_ATTR, "")].update({
            "regions": [e.text for e in info.findall("region")],
            "levels": [e.text for e in info.findall("level")],
            "used-ats": [e.text for e in info.findall("used-at")],
            "description": info.findtext("description"),
        })

    formats.append({
        "filename": path.name,
        "url": f"https://formats.debatekeeper.czlee.nz/v1/formats/{path.name}",
        "version": int(root.findtext("version")),
        "info": infos,
    })

formats.sort(key=lambda f: next(iter(f['info'].values()))['name'])

if args.add_errors:
    formats.extend([
        {
            "filename": "nosuchfile.xml",
            "url": "https://formats.debatekeeper.czlee.nz/v1/formats/nosuchfile.xml",
            "version": 1,
            "info": {"en": {
                "name": "ZZ Test - No such file",
                "regions": ["Nowhere"],
                "levels": ["None"],
                "used-ats": ["Nowhere"],
                "description": "Test entry to check what it does when the file doesn't exist",
            }},
        },
        {
            "filename": "wronghost.xml",
            "url": "https://czlee.github.io/debatekeeper-formats/v1/formats/wronghost.xml",
            "version": 1,
            "info": {"en": {
                "name": "ZZ Test - Wrong host",
                "regions": ["Nowhere"],
                "levels": ["None"],
                "used-ats": ["Nowhere"],
                "description": "Test entry to check what it does when the host is "
                               "different to what's expected",
            }},
        },
    ])

top = {"formats": formats}

with open(args.output_file, "w") as fp:
    json.dump(top, fp, indent=2)
