#!/usr/bin/env python
"""Configuration unit tests."""

import sys
import types

import pytest

sys.path.insert(0, "/home/gray/src/work/chcss")

from chcss import Config  # noqa: E402


def test_init_exists():
    """Test if Config().__init__() exists."""
    assert isinstance(Config.__init__, types.FunctionType)
