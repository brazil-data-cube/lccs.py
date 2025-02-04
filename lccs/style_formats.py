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
from .link import Link


class StyleFormats(dict):
    """Class."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with style format metadata.

        :param validate: true if the style format should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(StyleFormats, self).__init__(data or {})

    @property
    def id(self) -> int:
        """:return: the style format id."""
        return self['id']

    @property
    def name(self) -> str:
        """:return: the style format name."""
        return self['name']
    
    @property
    def links(self) -> list[Link]:
        """:return: a list of link in the classification system."""
        return [Link(link) for link in self['links']]
    
    def __repr__(self) -> str:
        """Return the string representation of a style format object."""
        text = f'Name:{self.name}'
        return text

    def __str__(self) -> str:
        """Return the string representation of a style format object."""
        return f'<Name:{self.name}>'


