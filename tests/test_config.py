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

"""Configuration unit tests."""

import types

import pytest

import chcss


def test_config_interface():
    """Test existence of functions and classes of the Config()."""
    assert isinstance(chcss.Config.__init__, types.FunctionType)
    assert isinstance(chcss.Config.__str__, types.FunctionType)
    assert isinstance(chcss.Config.__repr__, types.FunctionType)
    assert isinstance(chcss.Config.update, types.FunctionType)
    assert isinstance(chcss.Config.load, types.FunctionType)


def test_show_license_info(capsys):
    """Test ``--show-license`` and ``--show-warranty`` CLI options."""
    expected = """\
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

    with pytest.raises(SystemExit):
        conf = chcss.Config()
        conf.load(["--show-license"])

        actual = capsys.readouterr().out

        assert actual == expected

    with pytest.raises(SystemExit):
        conf = chcss.Config()
        conf.load(["--show-warranty"])

        actual = capsys.readouterr().out

        assert actual == expected
