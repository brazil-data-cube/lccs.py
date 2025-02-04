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
"""Python API client wrapper for LCCS-WS."""


class Link(dict):
    """Link object."""

    def __init__(self, data) -> None:
        """Initialize instance with dictionary data.

        :param data: Dict with Link metadata.
        """
        super(Link, self).__init__(data or {})

    @property
    def rel(self) -> str:
        """:return: the Link relation."""
        return self['rel']

    @property
    def href(self) -> str:
        """:return: the Link url."""
        return self['href']

    @property
    def type(self) -> str:
        """:return: the type of the Link object."""
        return self['type']

    @property
    def title(self)  -> str:
        """:return: the title of the Link object."""
        return self['title']
