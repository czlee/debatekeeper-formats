#!/usr/bin/env python
"""Validates debate format XML files against the schema."""

import argparse
import re
from pathlib import Path
import json
import requests

from lxml import etree


validator = etree.RelaxNG(etree.parse("schema-2.2.rng"))

LANG_ATTR = "{http://www.w3.org/XML/1998/namespace}lang"


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

    errors = validate_cross_references(path.name, root)
    errors += validate_multilingual_elements(path.name, root)

    if file_has_changed(path):
        errors += validate_version_number_has_changed(path)
    return errors


def validate_version_number_has_changed(path: Path, formats_list_path: Path = Path("v1/formats.json")) -> list[str]:
    filename = path.name
    root = etree.parse(open(path))

    extracted_version_number = int(root.find("version").text)  # the version number that is specified in the format xml

    formats = json.load(open(formats_list_path))["formats"]
    json_version_number = 0  # ensures that it is always defined, initialized to 0 to ensure that a new file also passes
    # grab the format in formats.json that matches the current one
    for format in formats:
        if format["filename"] == filename:
            json_version_number = format["version"]
            break

    if extracted_version_number <= json_version_number:
        return [f"Version number error in {filename}, version number has not changed."]

    return []


def file_has_changed(path: Path, formats_list_path: Path = Path("v1/formats.json")) -> bool:
    filename = path.name
    new_version = open(path).read()

    formats = json.load(open(formats_list_path))["formats"]
    # grab the format in formats.json that matches the current one
    for format in formats:
        if format["filename"] == filename:
            old_url = format["url"]
            break
    else:
        return True  # the fact it is not in formats.json yet means that it has been changed or is new

    # It feels somewhat hacky to get the old version this way but there doesn't seem to be an easy alternative
    response = requests.get(old_url)
    response.encoding = "UTF-8"
    old_version = response.text.replace("\r", "")

    return new_version != old_version


def validate_cross_references(filename: str, root: etree.ElementTree):
    """Checks the cross-references for period types and speech types, given the root of a debate
    format XML tree, and returns a list of errors. (If validation is successful, the list will be
    empty.)"""

    errors = []

    period_types = ["normal", "pois-allowed", "warning", "overtime", None]
    period_types.extend([pt.get("ref") for pt in get_period_type_elements(root)])

    for speech_type in root.find("speech-types").findall("speech-type"):
        errors += validate_attribute_xref(filename, speech_type, "first-period", period_types)
        for bell in speech_type.findall("bell"):
            errors += validate_attribute_xref(filename, bell, "next-period", period_types)

    speech_types = [st.get("ref") for st in root.find("speech-types").findall("speech-type")]

    for speech in root.find("speeches").findall("speech"):
        errors += validate_attribute_xref(filename, speech, "type", speech_types)

    return errors


def validate_attribute_xref(filename: str, element: etree.Element, attribute: str, allowed_values: list):
    value = element.get(attribute)
    if value not in allowed_values:
        return [f"Cross-ref error in {filename}, line {element.sourceline}: "
                f"unknown {attribute} {value!r}"]
    return []


def validate_multilingual_elements(filename, root):

    languages_element = root.find("languages")

    if languages_element is not None:
        languages = [e.text for e in languages_element.findall("language")]
    else:
        languages = None

    errors = []
    errors += validate_multilingual_element(filename, languages, root.getroot(), "name")
    errors += validate_multilingual_element(filename, languages, root.getroot(), "short-name",
                                            optional=True)
    errors += validate_multilingual_element(filename, languages, root.getroot(), "info")
    for period_type in get_period_type_elements(root):
        errors += validate_multilingual_element(filename, languages, period_type, "name")
        errors += validate_multilingual_element(filename, languages, period_type, "display")
    for speech_type in root.find("speech-types").findall("speech-type"):
        errors += validate_multilingual_element(filename, languages, speech_type, "name", optional=True)
    for speech in root.find("speeches").findall("speech"):
        errors += validate_multilingual_element(filename, languages, speech, "name")
    return errors


def validate_multilingual_element(filename: str, languages: list, element: etree.Element,
                                  subelement: str, optional=False):
    """Checks that the element given either has exactly one of the subelement, or every subelement
    has a unique language specifier."""
    errors = []
    children = element.findall(subelement)

    if len(children) == 0 and optional:
        return errors

    def add_error(el, message):
        errors.append(f"Multilingual error in {filename}, line {el.sourceline}: {message}")

    if languages is None:
        if len(children) > 1:
            add_error(children[1],
                f"Multiple {subelement} elements found, but no languages declared in file")
        for child in children:
            if child.get(LANG_ATTR):
                add_error(child,
                    f"Attribute 'lang' found in {subelement}, but no languages declared in file")

    else:
        found = dict.fromkeys(languages, False)
        for child in children:
            language = child.get(LANG_ATTR)
            if language is None:
                add_error(child, f"Language not specified with multiple {subelement} elements")
            elif language not in languages:
                add_error(child, f"Language {language!r} not declared in <languages>")
            elif found[language]:
                add_error(child, f"Language {language!r} found multiple times in {subelement} elements")
            found[language] = True

        for language in languages:
            if not found[language]:
                add_error(element, f"No translation for {subelement} found for language {language!r}")
    return errors


def validate_all_files(formats_dir):
    """Validates all files in the directory `formats_dir`."""
    if not formats_dir.is_dir():
        print(f"{formats_dir} is not a directory")
        return 1

    failures = []
    successes = []

    for child in formats_dir.iterdir():
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
        return 1

    else:
        print(f"All {len(successes)} files passed validation.")
        return 0


def check_for_wrongly_located_files(wrong_dirs, correct_dir):
    """Checks that no file in any directory in the list `wrong_dirs` looks like a debate format file."""

    pattern = re.compile(r"<\s*debate\-?format")
    wrong_files = []

    for wrong_dir in wrong_dirs:
        if wrong_dir.is_dir():
            for child in wrong_dir.iterdir():
                if child.is_file():
                    with open(child) as f:
                        if pattern.search(f.read(500)):
                            wrong_files.append(child)

    if wrong_files:
        print("Looks like the following files might be debate formats:")
        for filename in wrong_files:
            print(f" - {filename}")
        print(f"Did you mean to add them to the {correct_dir} directory instead?\n")
        return 1

    else:
        return 0


def get_period_type_elements(root):
    """Returns an iterable over custom period types, or an empty iterable if there aren't any."""
    period_types = root.find("period-types")
    if period_types is None:
        return []
    return period_types.findall("period-type")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formats_dir", nargs="?", default=Path("v1/formats"), type=Path)
    parser.add_argument("--wrong-dirs", nargs="?", default=[Path("."), Path("v1")], type=Path)
    args = parser.parse_args()

    return_code = check_for_wrongly_located_files(args.wrong_dirs, args.formats_dir)
    return_code += validate_all_files(args.formats_dir)
    exit(return_code)
