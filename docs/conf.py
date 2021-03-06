"""Sphinx configuration."""
# SPDX-License-Identifier: GPL-3.0-or-later
#
# chcss, a CSS naming hierarchy enforcer.
# Copyright (C) 2021 Jeremy A Gray <jeremy.a.gray@gmail.com>.

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information.

author = "Jeremy A Gray"
copyright = "2021, Jeremy A Gray"
project = "chcss"
release = "0.0.3"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

html_theme = "alabaster"
html_static_path = ["_static"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
