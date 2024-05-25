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

"""chcss module."""

from .config import Config
from .data import HTML5_ELEMENTS
from .data import HTML5_ELEMENTS_OBSOLETE
from .parser import main
from .parser import parse_class_name
