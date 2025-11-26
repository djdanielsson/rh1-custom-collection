#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Platform Team
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
name: text_filters
author: Platform Team
version_added: "1.0.0"
short_description: Text manipulation filters
description:
    - Provides custom text manipulation filters
    - Includes filters for formatting, transformation, and validation
filters:
    to_title_case:
        description: Convert string to title case
        type: string
    remove_special_chars:
        description: Remove special characters from string
        type: string
    truncate_string:
        description: Truncate string to specified length
        type: string
    slugify:
        description: Convert string to URL-friendly slug
        type: string
'''

import re


def to_title_case(text):
    """Convert string to title case"""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return text.title()


def remove_special_chars(text, replacement=''):
    """Remove special characters from string"""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return re.sub(r'[^a-zA-Z0-9\s]', replacement, text)


def truncate_string(text, length=50, suffix='...'):
    """Truncate string to specified length"""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if len(text) <= length:
        return text
    return text[:length-len(suffix)] + suffix


def slugify(text):
    """Convert string to URL-friendly slug"""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Convert to lowercase
    text = text.lower()

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove special characters
    text = re.sub(r'[^a-z0-9\-]', '', text)

    # Remove duplicate hyphens
    text = re.sub(r'-+', '-', text)

    # Strip leading/trailing hyphens
    text = text.strip('-')

    return text


class FilterModule(object):
    '''Custom text manipulation filters'''

    def filters(self):
        return {
            'to_title_case': to_title_case,
            'remove_special_chars': remove_special_chars,
            'truncate_string': truncate_string,
            'slugify': slugify,
        }



