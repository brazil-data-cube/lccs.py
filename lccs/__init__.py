#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
from .class_system import ClassSystem
from .classes import ClassSystemClass, ClassSystemClasses
from .lccs import lccs
from .link import Link
from .mappings import Mappings
from .utils import Utils
from .version import __version__

__all__ = ('__version__', 'lccs', )
