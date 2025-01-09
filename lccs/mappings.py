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
from .classes import ClassificationSystemClass


class MappingGroup(dict):
    """Group of class mappings."""

    def __init__(self, data: dict, validate: bool = False) -> None:
        """
        Initialize a MappingGroup with mapping data.

        :param data: Dictionary containing mapping group metadata.
        :param validate: Whether to validate the data using jsonschema. Default is False.
        """
        super().__init__(data or {})
        self._validate = validate

    @property
    def mappings(self) -> List["Mapping"]:
        """Return a list of mappings."""
        return [Mapping(mapping, self._validate) for mapping in self.get('mappings', [])]

    def _repr_html_(self) -> str:
        """Render an HTML representation of the mapping group."""
        return Utils.render_html('mapping.html', mappings=self)

    def __repr__(self) -> str:
        """Return a string representation of the mapping group."""
        return "\n\t".join(map(str, self.mappings))

    def __str__(self) -> str:
        """Return a human-readable string representation of the mapping group."""
        return "\n\t".join(map(str, self.mappings))


class Mapping(dict):
    """Representation of a single mapping."""

    def __init__(self, data: dict, validate: bool = False) -> None:
        """
        Initialize a Mapping with metadata.

        :param data: Dictionary containing mapping metadata.
        :param validate: Whether to validate the data using jsonschema. Default is False.
        """
        super().__init__(data or {})
        self._validate = validate
        self._initialize_classes()

    @property
    def degree_of_similarity(self) -> Optional[float]:
        """Return the degree of similarity."""
        return self.get('degree_of_similarity')

    @property
    def description(self) -> Optional[str]:
        """Return the description of the mapping."""
        return self.get('description')

    @property
    def link(self) -> List[dict]:
        """Return the links associated with the mapping."""
        return self.get('links', [])

    def _initialize_classes(self) -> None:
        """Initialize source and target classes from the mapping links."""
        for link in self.link:
            if link.get('rel') == 'item':
                if link.get('title') == 'Link to source class':
                    self['source_class'] = ClassificationSystemClass(Utils._get(link['href']))
                elif link.get('title') == 'Link to target class':
                    self['target_class'] = ClassificationSystemClass(Utils._get(link['href']))

    @property
    def source_class(self) -> Optional[ClassificationSystemClass]:
        """Return the source class."""
        return self.get('source_class')

    @property
    def target_class(self) -> Optional[ClassificationSystemClass]:
        """Return the target class."""
        return self.get('target_class')

    @property
    def source_class_id(self) -> Optional[int]:
        """Return the ID of the source class."""
        return self.get('source_class_id')

    @property
    def target_class_id(self) -> Optional[int]:
        """Return the ID of the target class."""
        return self.get('target_class_id')

    def __repr__(self) -> str:
        """Return a string representation of the mapping."""
        return (
            f"{self.source_class.title if self.source_class else 'Unknown Source'} -> "
            f"{self.target_class.title if self.target_class else 'Unknown Target'} - "
            f"Degree of Similarity: {self.degree_of_similarity}"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of the mapping."""
        return self.__repr__()




