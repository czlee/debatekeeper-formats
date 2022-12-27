#!/usr/bin/env python
"""Checks for debate format files that might be in the wrong directories."""

import argparse
import re
from pathlib import Path


CORRECT_DIR = "v1/formats"
WRONG_DIRS = [
    Path("."),
    Path("v1"),
]


def check_for_wrongly_located_files() -> int:
    """Checks that no file in any directory in the list `wrong_dirs` looks like a debate format file."""

    pattern = re.compile(r"<\s*debate\-?format")
    wrong_files = []

    for wrong_dir in WRONG_DIRS:
        for child in wrong_dir.iterdir():
            if child.is_file():
                with open(child) as f:
                    if pattern.search(f.read(500)):
                        wrong_files.append(child)

    if wrong_files:
        print("❌ Looks like the following files might be debate formats:")
        for filename in wrong_files:
            print(f" - {filename}")
        print(f"Did you mean to add them to the {CORRECT_DIR} directory instead?\n")
        return 1

    else:
        return 0


if __name__ == "__main__":

    # no arguments, this is just for the help documentation
    argparse.ArgumentParser(description=__doc__).parse_args()

    return_code = check_for_wrongly_located_files()
    exit(return_code)
