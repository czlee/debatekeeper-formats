#!/usr/bin/env python
"""Updates the list in formats.json. Should be run after any updates to formats, and the result
committed to the repository."""

import argparse
import json
from lxml import etree
from pathlib import Path

from validate import validate_file

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("formats_dir", nargs="?", default=Path("v1/formats"), type=Path)
parser.add_argument("-O", "--output-file", default="v1/formats.json")
parser.add_argument("--add-errors", action="store_true",
    help="Adds some erroneous entries to test error conditions in the app")
args = parser.parse_args()

if not args.formats_dir.is_dir():
    print(f"{formats_dir} is not a directory")
    exit(1)

formats = []

for child in args.formats_dir.iterdir():
    if child.suffix != ".xml":
        print(f"skipping {child}")
        continue

    errors = validate_file(child)
    if errors:
        print("\n".join(errors))

    child_root = etree.parse(open(child))

    infos = child_root.findall("info")
    formats.append({
        "filename": child.name,
        "url": f"https://formats.debatekeeper.czlee.nz/v1/formats/{child.name}",
        "version": int(child_root.find("version").text),
        "info": {info.get("{http://www.w3.org/XML/1998/namespace}lang", ""): {
            "name": child_root.find("name").text,
            "regions": [e.text for e in info.findall("region")],
            "levels": [e.text for e in info.findall("level")],
            "used-ats": [e.text for e in info.findall("used-at")],
            "description": info.find("description").text,
        } for info in infos}
    })

formats.sort(key=lambda f: next(iter(f['info'].values()))['name'])

if args.add_errors:
    formats.extend([{
        "filename": "nosuchfile.xml",
        "url": "https://formats.debatekeeper.czlee.nz/formats/nosuchfile.xml",
        "version": 1,
        "info": {"en": {
            "name": "No such file",
            "regions": ["Nowhere"],
            "levels": ["None"],
            "used-ats": ["Nowhere"],
            "description": "Test entry to check what it does when the file doesn't exist"
        }},
      },
      {
        "filename": "wronghost.xml",
        "url": "https://czlee.github.io/debatekeeper-formats/formats/wronghost.xml",
        "version": 1,
        "info": {"en": {
            "name": "Wrong host",
            "regions": ["Nowhere"],
            "levels": ["None"],
            "used-ats": ["Nowhere"],
            "description": "Test entry to check what it does when the host is different to what's expected"
        }},
    }])

with open(args.output_file, "w") as fp:
    json.dump(formats, fp, indent=2)
