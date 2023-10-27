#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Python Client Library for the LCCS Web Service."""
from .lccs import LCCS
from .classification_system import ClassificationSystem
from . import cli
from .classes import ClassificationSystemClass
from .mappings import Mapping, MappingGroup
from .utils import Utils
from .style_utils import SldGenerator
from .version import __version__
from .lccs import LCCS

__all__ = ('__version__',
           'lccs', )
