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
from typing import List, Optional
from .utils import Utils


class ClassesGroup(dict):
    """Group of classification system classes."""

    def __init__(self, data: dict, validate: bool = False) -> None:
        """
        Initialize instance with dictionary data.

        :param data: Dictionary containing classification group data.
        :param validate: Whether to validate the data using jsonschema. Default is False.
        """
        super().__init__(data or {})
        self._validate = validate
        self._classes: List[ClassificationSystemClass] = [
            ClassificationSystemClass(i, self._validate) for i in self.get('classes', [])
        ]

    @property
    def classes(self) -> List['ClassificationSystemClass']:
        """Return the list of classification system classes."""
        return self._classes

    def _repr_html_(self) -> str:
        """Render HTML representation."""
        return Utils.render_html('mapping.html', mappings=self)

    def __repr__(self) -> str:
        """Return the string representation of the group."""
        return "\n".join([str(cls) for cls in self._classes])

    def __str__(self) -> str:
        """Return the string representation of the group (readable)."""
        return self.__repr__()


class ClassificationSystemClass(dict):
    """Class representing a classification system."""

    def __init__(self, data: dict, validate: bool = False) -> None:
        """
        Initialize instance with dictionary data.

        :param data: Dictionary containing class metadata.
        :param validate: Whether to validate the data using jsonschema. Default is False.
        """
        super().__init__(data or {})
        self._validate = validate

    @property
    def id(self) -> str:
        """Return the class ID."""
        return self.get('id')

    @property
    def name(self) -> str:
        """Return the class name."""
        return self.get('name')

    @property
    def title(self) -> str:
        """Return the class title."""
        return self.get('title')

    @property
    def description(self) -> Optional[str]:
        """Return the class description."""
        return self.get('description')

    @property
    def color(self) -> Optional[str]:
        """Return the class color."""
        return self.get('color')

    @property
    def code(self) -> str:
        """Return the class code."""
        return self.get('code')

    @property
    def links(self) -> List[dict]:
        """Return the class links."""
        return self.get('links', [])

    @property
    def class_parent_id(self) -> Optional[str]:
        """Return the parent class ID."""
        return self.get('class_parent_id')

    @property
    def class_parent_name(self) -> Optional[str]:
        """Return the parent class name."""
        return self._get_parent_name()

    def _get_parent_name(self) -> Optional[str]:
        """Resolve and return the parent class name, if available."""
        if self.class_parent_id:
            parent_link = next((link for link in self.links if link.get('rel') == 'parent'), None)
            if parent_link:
                try:
                    parent_url = self._build_parent_url(parent_link['href'])
                    parent_data = Utils._get(parent_url)
                    return ClassificationSystemClass(parent_data).name
                except Exception as e:
                    return None
        return None

    def _build_parent_url(self, href: str) -> str:
        """Build the full URL for the parent class."""
        system = href.rsplit('/', maxsplit=1)[1].split('?')[0]
        token = href.split('?')[-1] if '?' in href else ""
        base_url = href.rsplit('/', maxsplit=1)[0]
        return f"{base_url}/{system}/classes/{self['class_parent_id']}?{token}" if token else f"{base_url}/{system}/classes/{self['class_parent_id']}"
