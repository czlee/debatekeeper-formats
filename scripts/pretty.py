#!/usr/bin/env python
"""Prettifies an XML file."""

import argparse

from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

root = etree.parse(args.filename)

print(etree.tostring(root, pretty_print=True, encoding='utf-8').decode())
