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

"""chcss configuration functions."""


import argparse
import json
import os
import re
import sys
import textwrap

import toml

from .data import HTML5_ELEMENTS

# from .data import HTML5_ELEMENTS_OBSOLETE


class Config:
    """Class for accessing and loading chcss configuration options.

    Provides default values for all chcss configuration options and
    loading methods for reading pyproject.toml/package.json and CLI
    options.

    Attributes
    ----------
    fn : string
        Name of file to be checked; default is ``STDIN``.
    config_file : string
        Configuration file path; default is ``pyproject.toml``.
    namespaces : [string]
        List of project namespaces; default is ``[]``.
    functions : [string]
        List of project functions; default is ``[]``.
    components : [string]
        List of project components; default is ``[]``.
    elements : [string]
        List of project elements; default is the list of HTML5 elements.
    modifiers : [string]
        List of project modifiers; default is ``[]``.
    """

    def __init__(
        self,
        fn="",
        config_file="./pyproject.toml",
        namespaces=[],
        functions=[],
        components=[],
        elements=HTML5_ELEMENTS,
        modifiers=[],
    ):
        """Create a ``Config()`` object.

        Create a default ``Config()`` object.

        Returns
        -------
        object
            A Config() object.
        """
        self.fn = fn
        self.config_file = config_file
        self.namespaces = namespaces
        self.functions = functions
        self.components = components
        self.elements = elements
        self.modifiers = modifiers

    def __str__(self):
        """Stringify a ``Config()`` object.

        String representation of a ``Config()`` object, as the
        ``[tool.chcss]`` section of a pyproject.toml file.

        Returns
        -------
        string
            The current configuration, as the [tool.chcss] section of a
            ``pyproject.toml`` file.
        """
        rs = "[tool.chcss]\n"
        rs += "\n"

        configs = [
            "namespaces",
            "functions",
            "components",
            "elements",
            "modifiers",
        ]

        for x in configs:
            rs += "namespaces = [\n" + ",\n".join(
                map(lambda item: f'  "{item}"', getattr(self, x))
            )

            if len(getattr(self, x)):
                rs += "\n]\n\n"
            else:
                rs += "]\n\n"

        return rs

    def __repr__(self):
        """Representation of a ``Config()`` object."""
        return (
            f'Config(fn="{self.fn}", '
            f'config_file="{self.config_file}", '
            f"namespaces={self.namespaces}, "
            f"functions={self.functions}, "
            f"components={self.components}, "
            f"elements={self.elements}, "
            f"modifiers={self.modifiers}, "
        )

    def update(self, *args, **kwargs):  # dead:  disable
        """Update a configuration.

        Update the current configuration object from the provided
        dictionary, ignoring any keys that are not attributes and
        values that are ``None``.  The provided key/value pairs
        override the original values in self.

        Parameters
        ----------
        kwargs : dict
           Key/value pairs of configuration options.
        """
        for k, v in kwargs.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

        return

    # def validate(self):
    #     """Validate a configuration.

    #     Validate the current configuration object to ensure compliance
    #     with the conventional commit specification.  Current checks
    #     include: ensure that 'fix' and 'feat' are present in the
    #     ``types`` list.

    #     Returns
    #     -------
    #     boolean
    #         True for a valid configuration, raises on invalid
    #         configuration.

    #     Raises
    #     ------
    #     ValueError
    #         Indicates a configuration value is incorrect.
    #     """
    #     if not ("fix" in self.types and "feat" in self.types):
    #         raise ValueError("Commit types must include 'fix' and 'feat'.")

    #     return True

    def load(self, argv=None):
        """Load configuration options.

        Load configuration options from defaults (class constructor),
        file (either default or specified on CLI), then CLI, with
        later values overriding previous values.

        Unset values are explicitly ``None`` at each level.

        Handles any ``FileNotFound``, ``JSONDecodeError``, or
        ``TomlDecodeError`` exceptions that arise during loading of
        configuration file by ignoring the file.
        """
        # Parse the CLI options to make configuration file path available.
        args = _create_argument_parser().parse_args(argv)

        # Configuration file; override defaults.
        if args.config_file is not None:
            self.config_file = args.config_file

        try:
            self.update(**_load_file(self.config_file))
        except (FileNotFoundError,):
            print(
                f"Unable to find configuration file {self.config_file},"
                " using defaults and CLI options."
            )
        except (json.JSONDecodeError,):
            print(
                f"Unable to parse configuration file {self.config_file}"
                " (default package.json), using defaults and CLI options.\n"
                "Ensure that file format matches extension."
            )
        except (toml.TomlDecodeError,):
            print(
                f"Unable to parse configuration file {self.config_file}"
                " (default pyproject.toml), using defaults and CLI options."
                "  Ensure that file format matches extension."
            )

        self.update(**vars(args))

        return


def _load_file(filename="./pyproject.toml"):
    """Load a configuration file, using the ``[tool.chcss]`` section.

    Load a ``pyproject.toml`` configuration file, using the
    ``[tool.chcss]`` section, or a ``package.json`` configuration file,
    using the ``chcss`` entry.  Will only load ``package.json`` if
    ``pyproject.toml`` is not available or if ``package.json`` is
    explicitly set as the configuration file.

    Parameters
    ----------
    filename : string (optional)
        Configuration file to load.

    Returns
    -------
    dict
       Configuration option keys and values, with unset values
       explicitly set to ``None``.

    Raises
    ------
    JSONDecodeError
        Raised if there are problems decoding a JSON configuration
        file.
    TomlDecodeError
        Raised if there are problems decoding a TOML configuration
        file.
    FileNotFoundError
        Raised if the configuration file does not exist or is not
        readable.
    """
    options = {}
    jsonRE = re.compile(r"^.*\.json$", re.IGNORECASE)

    if os.path.abspath(filename) == os.path.abspath("./pyproject.toml"):
        try:
            # Default to ``./pyproject.toml``.
            options = _load_toml_file(filename)
        except toml.TomlDecodeError:
            raise
        except FileNotFoundError:
            try:
                # Then try ``./package.json``.
                options = _load_json_file("./package.json")
            except json.JSONDecodeError:
                raise
            except FileNotFoundError:
                raise
    elif jsonRE.match(filename):
        try:
            # Well, if JSON is supplied, use it.
            options = _load_json_file(filename)
        except json.JSONDecodeError:
            raise
        except FileNotFoundError:
            raise
    else:
        try:
            # Last chance, parse filename as TOML.
            options = _load_toml_file(filename)
        except toml.TomlDecodeError:
            raise
        except FileNotFoundError:
            raise

    return options


def _load_json_file(filename="./package.json"):
    """Load a JSON configuration file, using the ``chcss`` entry.

    Load a ``package.json`` configuration file, returning the ``chcss``
    entry.

    Parameters
    ----------
    filename : string (optional)
        Configuration file to load.

    Returns
    -------
    dict
       Configuration option keys and values, with unset values
       explicitly set to ``None``.

    Raises
    ------
    JSONDecodeError
        Raised if there are problems decoding a JSON configuration
        file.
    FileNotFoundError
        Raised if the configuration file does not exist or is not
        readable.
    """
    try:
        with open(filename, "r") as file:
            config = json.load(file)
    except json.JSONDecodeError as error:
        lines = error.doc.split("\n")
        print(
            f"In configuration file {filename},"
            f" line {error.lineno}, column {error.colno}:"
        )
        print(lines[error.lineno - 1])
        print(error.msg)
        raise
    except FileNotFoundError as error:
        print(f"{error.strerror}: {error.filename}")
        raise

    empty_options = {
        "fn": None,
        "config_file": None,
        "namespaces": None,
        "functions": None,
        "components": None,
        "elements": None,
        "modifiers": None,
    }

    for k, v in config["chcss"].items():
        empty_options[k] = v

    return empty_options


def _load_toml_file(filename="./pyproject.toml"):
    """Load a toml configuration file.

    Load a ``pyproject.toml`` configuration file, returning the
    ``[tool.chcss]`` section.

    Parameters
    ----------
    filename : string (optional)
        Configuration file to load.

    Returns
    -------
    dict
       Configuration option keys and values, with unset values
       explicitly set to ``None``.

    Raises
    ------
    TomlDecodeError
        Raised if there are problems decoding a TOML configuration
        file.
    FileNotFoundError
        Raised if the configuration file does not exist or is not
        readable.
    """
    try:
        with open(filename, "r") as file:
            config = toml.load(file)
    except toml.TomlDecodeError as error:
        lines = error.doc.split("\n")
        print(
            f"In configuration file {filename},"
            f" line {error.lineno}, column {error.colno}:"
        )
        print(lines[error.lineno - 1])
        print(error.msg)
        raise
    except FileNotFoundError as error:
        print(f"{error.strerror}: {error.filename}")
        print("trying package.json...")
        raise

    empty_options = {
        "fn": None,
        "config_file": None,
        "namespaces": None,
        "functions": None,
        "components": None,
        "elements": None,
        "modifiers": None,
    }

    for k, v in config["tool"]["chcss"].items():
        empty_options[k] = v

    return empty_options


def _create_argument_parser():
    """Create an argparse argument parser."""
    parser = argparse.ArgumentParser(
        description="""\
This program comes with ABSOLUTELY NO WARRANTY; for details type
``chcss --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``chcss
--show-license`` for details.
""",
    )

    parser.add_argument(
        "--show-warranty",
        nargs=0,
        action=_ShowLicenseAction,
        help="Show warranty information.",
    )

    parser.add_argument(
        "--show-license",
        nargs=0,
        action=_ShowLicenseAction,
        help="Show license information.",
    )

    parser.add_argument(
        dest="fn",
        type=str,
        default="-",
        nargs="?",
        help="Name of file to be checked.",
    )

    parser.add_argument(
        "-o",
        "--config-file",
        dest="config_file",
        type=str,
        default="./pyproject.toml",
        help="Path to configuration file.  Default is ./pyproject.toml.",
    )

    list_options = [
        "namespaces",
        "functions",
        "components",
        "modifiers",
    ]

    for opt in list_options:
        parser.add_argument(
            f"-{opt[:1]}",
            f"--{opt}",
            dest=f"{opt}",
            default=None,
            type=_field_list_handler,
            help=f"List (comma delimited) of allowable {opt} for the"
            f" {opt[:-1]} segment of the identifier.  Default is an empty list.",
        )

    parser.add_argument(
        "-e",
        "--elements",
        dest="elements",
        default=None,
        type=_field_list_handler,
        help="List (comma delimited) of allowable elements for the"
        " element segment of the identifier.  Default is the HTML5 tag list.",
    )

    return parser


class _ShowLicenseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # dead:  disable
        license = """\
chcss:  CSS naming hierarchy enforcer.

Copyright (C) 2021 Jeremy A Gray <jeremy.a.gray@gmail.com>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
        print(
            "\n\n".join(
                list(
                    map(
                        lambda item: "\n".join(textwrap.wrap(item.strip(), 72)),
                        textwrap.dedent(license).strip().split("\n\n"),
                    )
                )
            )
        )

        sys.exit(0)


def _field_list_handler(s):
    if len(s) == 0:
        return []
    else:
        return [item.strip() for item in s.split(",")]
