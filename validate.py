#!/usr/bin/env python
"""Validates debate format XML files against the schema."""

import argparse
import json
from lxml import etree
from pathlib import Path


validator = etree.RelaxNG(etree.parse("schema-2.2.rng"))


def validate_file(path):
    """Validates the file given by the path `path`, and returns a list of syntax, validation or
    cross-reference errors. (If validation is successful, the list will be empty.)"""

    try:
        root = etree.parse(open(path))
    except etree.XMLSyntaxError as e:
        error = f"XML syntax error in {path.name}: {e}"
        return [error]

    if not validator.validate(root):
        errors = [f"Validation error in {path.name}, line {err.line}, column {err.column}: "
                  f"{err.message}" for err in validator.error_log]
        return errors

    errors = validate_cross_references(path, root)
    return errors


def validate_cross_references(path, root):
    """Checks the cross-references for period types and speech types, given the root of a debate
    format XML tree, and returns a list of errors. (If validation is successful, the list will be
    empty.)"""

    errors = []

    period_types = ["normal", "pois-allowed", "warning", "overtime", None]

    custom_period_types = root.find("period-types")
    if custom_period_types is not None:
        period_types.extend([pt.get("ref") for pt in custom_period_types.findall("period-type")])

    for speech_type in root.find("speech-types").findall("speech-type"):

        if speech_type.get("first-period") not in period_types:
            errors.append(f"Cross-ref error in {path.name}: speech type '{speech_type.get('ref')}' "
                          f"has unknown first-period '{speech_type.get('first-period')}'")

        for bell in speech_type.findall("bell"):
            if bell.get("next-period") not in period_types:
                errors.append(f"Cross-ref error in {path.name}: bell at '{bell.get('time')}' in "
                              f"speech type '{speech_type.get('ref')}' has unknown next-period "
                              f"'{bell.get('next-period')}'")

    speech_types = [st.get("ref") for st in root.find("speech-types").findall("speech-type")]

    for speech in root.find("speeches").findall("speech"):
        if speech.get("type") not in speech_types:
            errors.append(f"Cross-ref error in {path.name}: speech '{speech.find('name').text}' "
                          f"has unknown speech type '{speech.get('type')}'")

    return errors


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formats_dir", nargs="?", default=Path("formats"), type=Path)
    args = parser.parse_args()

    if not args.formats_dir.is_dir():
        print(f"{formats_dir} is not a directory")
        exit(1)

    failures = []
    successes = []

    for child in args.formats_dir.iterdir():
        if child.suffix != ".xml":
            print(f"skipping {child}")
            continue

        errors = validate_file(child)
        if errors:
            print("\n".join(errors))
            failures.append(child)
        else:
            successes.append(child)

    if failures:
        print(f"\n{len(successes)} files passed validation.")
        print(f"\nValidation failures in the following {len(failures)} files:")
        for failure in failures:
            print(f" - {failure}")
        exit(1)

    else:
        print(f"All {len(successes)} files passed validation.")