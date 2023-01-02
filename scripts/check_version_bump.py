#!/usr/bin/env python
"""Checks that the version numbers of all changed files have been incremented."""


import argparse
import subprocess
from pathlib import Path

from lxml import etree


class VersionNumberError(RuntimeError):
    pass


def validate_version_numbers(formats_dir: Path, base_ref: str) -> int:
    if not formats_dir.is_dir():
        print(f"{formats_dir} is not a directory")
        return 1

    diff_output = subprocess.check_output(["git", "diff", "--name-only", base_ref, "--", formats_dir], text=True)
    changed_files = [Path(file) for file in diff_output.split()]

    if not changed_files:
        print(f"🆗 No debate format files have changed since {base_ref}")

    nerrors = 0
    for path in changed_files:
        nerrors += check_version_number_increment(path, base_ref)

    return nerrors


def check_version_number_increment(path: Path, base_ref: str) -> list[str]:
    """Validates that the version number in the file given by the path `path` has changed, by
    comparing it to the version number in the same file of the commit given by `base_ref`. The
    validation passes if no `base_ref` is given, or if the file has not changed."""
    filename = path.name

    new_content = open(path, 'rb').read()
    try:
        original_content = subprocess.check_output(["git", "show", f"{base_ref}:{path}"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"🛑 {filename} ERROR: Error getting original contents: {e}")
        return 1

    try:
        new_version = extract_version_number(new_content)
        original_version = extract_version_number(original_content)
    except VersionNumberError as e:
        print(f"🛑 {filename} ERROR: {e}")
        return 1

    if new_version <= original_version:
        print(f"❌ {filename} ERROR: File has changed so expected at least {original_version+1}, found "
              f"'{new_version}'")
        return 1
    else:
        print(f"✅ {filename}: Version has changed from {original_version} to {new_version}")
        return 0


def extract_version_number(contents: str):
    try:
        root = etree.fromstring(contents)
    except etree.XMLSyntaxError as e:
        raise VersionNumberError(f"Invalid XML: {e}")

    element = root.find("version")
    if element is None:
        raise VersionNumberError("No <version> element found")
    if element.text is None:
        raise VersionNumberError("<version> element has no text")

    try:
        version = int(element.text)
    except ValueError:
        raise VersionNumberError(f"Couldn't parse number '{element.text}'")

    return version


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formats_dir", nargs="?", default=Path("v1/formats"), type=Path)
    parser.add_argument("--base-ref", default="origin/main", help="Git commit-ish")
    args = parser.parse_args()

    return_code = validate_version_numbers(args.formats_dir, args.base_ref)
    exit(return_code)
