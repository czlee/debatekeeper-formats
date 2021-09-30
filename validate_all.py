#!/usr/bin/env python
"""Updates the list in formats.json. Should be run after any updates to formats, and the result
committed to the repository."""

import argparse
import json
from lxml import etree
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("formats_dir", nargs="?", default=Path("formats"), type=Path)
args = parser.parse_args()

if not args.formats_dir.is_dir():
    print(f"{formats_dir} is not a directory")
    exit(1)

validator = etree.RelaxNG(etree.parse("schema-2.2.rng"))

failures = []

for child in args.formats_dir.iterdir():
    if child.suffix != ".xml":
        print(f"skipping {child}")
        continue

    try:
        child_root = etree.parse(open(child))
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error in {child.name}: {e}")
        failures.append(child)
        continue

    if not validator.validate(child_root):
        for error in validator.error_log:
            print(f"Validation error in {child.name}, line {error.line}, column {error.column}: {error.message}")
        failures.append(child)

if failures:
    print("\nValidation failures in the following files:")
    for failure in failures:
        print(f" - {failure}")
    exit(1)

else:
    print("All files validated.")