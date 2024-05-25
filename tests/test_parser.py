# ******************************************************************************
#
# chcss, a CSS naming hierarchy enforcer.
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
#
# All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# ******************************************************************************

"""Parser unit tests."""

import types

import chcss


def test_parser_interface():
    """Test existence of functions and classes of the parser."""
    assert isinstance(chcss.main, types.FunctionType)
    assert isinstance(chcss.parse_class_name, types.FunctionType)


def test_parse_class_name():
    """Test parse_class_name()."""
    names = [
        # Namespaces and functions.
        ("gf_accounts-c", True),
        ("gf_blog-c", True),
        ("gf_content-c", True),
        ("gf_news-c", True),
        ("gfaccounts-c", False),
        ("gfblog-c", False),
        ("gfcontent-c", False),
        ("gfnews-c", False),
        ("gf_accounts-d", False),
        ("gf_blog-d", False),
        ("gf_content-d", False),
        ("gf_news-d", False),
        # With components.
        ("gf_news-c-navbar", True),
        ("gf_news-c-footer", True),
        ("gfnews-c-navbar", False),
        ("gfnews-c-footer", False),
        ("gfnews-c-form", False),
        # With multiple components.
        ("gf_news-c-navbar-list", True),
        ("gf_news-c-list-navbar", True),
        ("gf_news-c-footer-list", True),
        ("gfnews-c-navbar-form", False),
        ("gfnews-c-form-navbar", False),
        # With elements.
        ("gf_news-c-navbar-ul", True),
        ("gf_news-c-navbar-li", True),
        ("gf_news-c-navbar-a", True),
        ("gf_news-c-navbar-ul-li", False),
        ("gf_news-c-navbar-ul-li-a", False),
        # With modifiers.
        ("gf_news-c-navbar-ul-reverse", True),
        ("gf_news-c-navbar-li-reverse", True),
        ("gf_news-c-navbar-a-reverse", True),
        ("gf_news-c-navbar-ul-li-a-reverse", False),
        ("gf_news-c-navbar-ul-inverse", False),
        ("gf_news-c-navbar-li-inverse", False),
        ("gf_news-c-navbar-a-inverse", False),
        ("gf_news-c-navbar-ul-li-a-inverse", False),
        # With extras.
        ("gf_news-c-navbar-ul-reverse-double", False),
        ("gf_news-c-navbar-li-reverse-double", False),
        ("gf_news-c-navbar-a-reverse-double", False),
        ("gf_news-c-navbar-ul-li-a-reverse-double", False),
    ]

    for name in names:
        assert chcss.parse_class_name(name[0]) is name[1]
