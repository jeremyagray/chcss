# SPDX-License-Identifier: GPL-3.0-or-later
#
# chcss, a CSS naming hierarchy enforcer.
# Copyright (C) 2021 Jeremy A Gray <jeremy.a.gray@gmail.com>.
"""chcss parser functions and classes."""

import pyparsing as pp


def parse_class_name(name):
    """Parse a CSS class identifier.

    Parse a CSS class identifier for generation of the CSS class
    identifier hierarchy.

    namespace-function((-component)+(-element(-modifier)*)?)?

    BNF for Identifier::

        namespace:: ( 'user defined word' )
        function:: ( 'user defined function' )
        component:: ( 'user defined component' )
        element:: ( 'HTML element' )
        modifier:: ( 'user defined modifier' )
        identifier:: namespace-function((-component)+(-element(-modifier)*)?)?

    Parameters
    ----------
    name : string
        The identifier to be parsed.

    Returns
    -------
    dict
        Data returned from parsing.

    Raises
    ------
    ParseException
        Indicate a ``name`` that is not parseable in the current
        configuration.
    """
    # Basic temporary configuration.
    namespaces = [
        "gf_accounts",
        "gf_blog",
        "gf_content",
        "gf_news",
    ]
    functions = [
        "c",
        "l",
    ]
    components = [
        "navbar",
        "footer",
        "list",
    ]
    elements = [
        "a",
        "ul",
        "li",
    ]
    modifiers = [
        "reverse",
    ]

    namespace = pp.oneOf(namespaces)
    function = pp.oneOf(functions)
    component = pp.oneOf(components)
    element = pp.oneOf(elements)
    modifier = pp.oneOf(modifiers)

    # identifier:: namespace-function((-component)+(-element(-modifier)*)?)?
    identifier = pp.Group(
        namespace
        + "-"
        + function
        + pp.Optional(
            pp.OneOrMore("-" + component)
            + pp.Optional("-" + element + pp.ZeroOrMore("-" + modifier))
        )
    )

    try:
        print(name, identifier.parseString(name, parseAll=True))
        return True
    except pp.ParseException as error:
        print(error)
        return False


def main(args):
    """Validate the CSS class hierarchy of a file."""
    pass
