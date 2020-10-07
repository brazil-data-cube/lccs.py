#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
from .lccs import LCCS
from .class_system import ClassificationSystem
from .classes import ClassificationSystemClass
from .mappings import Mapping, MappingGroup
from .utils import Utils
from .version import __version__
from .lccs import LCCS

__all__ = ('__version__',
           'lccs', )
