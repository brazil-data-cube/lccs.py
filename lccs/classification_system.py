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
from typing import Any, List, Optional, Union

from .classes import ClassesGroup, ClassificationSystemClass
from .link import Link
from .utils import Utils


class ClassificationSystem(dict):
    """Representation of a Classification System."""

    def __init__(self, data: dict, validate: bool = False) -> None:
        """
        Initialize a classification system with metadata.

        :param data: Dictionary containing classification system metadata.
        :param validate: Whether to validate the data using jsonschema. Default is False.
        """
        super().__init__(data or {})
        self._validate = validate

    @property
    def id(self) -> int:
        """Return the ID of the classification system."""
        return self.get('id')

    @property
    def identifier(self) -> str:
        """Return the identifier of the classification system."""
        return self.get('identifier')

    @property
    def name(self) -> str:
        """Return the name of the classification system."""
        return self.get('name')

    @property
    def title(self) -> str:
        """Return the title of the classification system."""
        return self.get('title')

    @property
    def links(self) -> List[Link]:
        """Return a list of links associated with the classification system."""
        return [Link(link) for link in self.get('links', [])]

    @property
    def description(self) -> Optional[str]:
        """Return the description of the classification system."""
        return self.get('description')

    @property
    def version(self) -> str:
        """Return the version of the classification system."""
        return self.get('version')

    @property
    def authority_name(self) -> Optional[str]:
        """Return the authority name of the classification system."""
        return self.get('authority_name')

    def classes(
        self,
        class_name_or_id: Optional[str] = None,
        style_format_name_or_id: Optional[str] = None
    ) -> Union[ClassesGroup, ClassificationSystemClass]:
        """
        Return the classes of the classification system.

        :param class_name_or_id: Name or ID of a specific class. Default is None.
        :param style_format_name_or_id: Style format ID for filtering classes. Default is None.
        :return: A group of classes or a specific classification system class.
        """
        try:
            classes_url = next(
                link['href'] for link in self.get('links', []) if link.get('rel') == 'classes'
            )

            params = {}
            if style_format_name_or_id:
                params["style_format_id"] = style_format_name_or_id

            classes_data = Utils._get(classes_url, params=params)

            if class_name_or_id:
                specific_class_url = f"{classes_url}/{class_name_or_id}"
                specific_class_data = Utils._get(specific_class_url, params=params)
                return ClassificationSystemClass(specific_class_data, self._validate)

            all_classes = ClassesGroup({"classes": classes_data})
            return all_classes.classes

        except StopIteration:
            raise ValueError("No 'classes' link found in the classification system.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while retrieving classes: {e}")

    def _repr_html_(self) -> str:
        """Render an HTML representation of the classification system."""
        return Utils.render_html('classification_system.html', classification_system=self)

    def __repr__(self) -> str:
        """Return the string representation of the classification system."""
        return f'{self.id}:{self.name}-{self.version} - Title: {self.title}'

    def __str__(self) -> str:
        """Return a human-readable string representation of the classification system."""
        return f'<Classification System [{self.id}:{self.name}-{self.version} - Title: {self.title}]>'
