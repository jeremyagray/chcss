#!/usr/bin/env python
"""Parser unit tests."""

import sys
import types

import pytest

sys.path.insert(0, "/home/gray/src/work/chcss")

from chcss import parser  # noqa: E402


def test_parser_exists():
    """Test if parser() exists."""
    assert isinstance(parser, types.FunctionType)
