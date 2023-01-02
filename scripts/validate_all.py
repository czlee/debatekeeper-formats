#!/usr/bin/env python
"""Intended as a convenience script for developers to run all validations locally. Not run by CI."""

import argparse
from pathlib import Path

from check_version_bump import validate_version_numbers
from check_wrongly_located_files import check_for_wrongly_located_files
from validate_xml_schema import validate_xml_schema_for_all_files

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("formats_dir", nargs="?", default=Path("v1/formats"), type=Path)
parser.add_argument("--base-ref", default="origin/main")
args = parser.parse_args()


def print_heading(heading, first=False):
    if not first:
        print()
    print(f"\033[1;36m=== {heading} ===\033[0m")


print_heading("Validate XML files against schema", first=True)
return_code = validate_xml_schema_for_all_files(args.formats_dir)

print_heading(f"Validate version numbers against {args.base_ref}")
return_code += validate_version_numbers(args.formats_dir, args.base_ref)

print_heading("Check for wrongly located files")
return_code += check_for_wrongly_located_files()

exit(return_code)
