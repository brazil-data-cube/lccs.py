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
from typing import Union, Any, List, Optional, cast

from .classes import ClassificationSystemClass, ClassesGroup
from .link import Link
from .utils import Utils


class ClassificationSystem(dict):
    """Classification System Class."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with class system metadata.
        :param validate: true if the Class System should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(ClassificationSystem, self).__init__(data or {})

    @property
    def id(self) -> int:
        """:return: id of classification system."""
        return self['id']

    @property
    def identifier(self) -> str:
        """:return: identifier of classification system."""
        return self['identifier']

    @property
    def name(self) -> str:
        """:return: name of classification system."""
        return self['name']

    @property
    def title(self) -> str:
        """:return: title of classification system."""
        return self['title']

    @property
    def links(self) -> List[Link]:
        """:return: a list of link in the classification system."""
        return [Link(link) for link in self['links']]

    @property
    def description(self) -> str:
        """:return: description of classification system."""
        return self['description']

    @property
    def version(self) -> str:
        """:return: version of classification system."""
        return self['version']

    @property
    def authority_name(self) -> str:
        """:return: authority_name of classification system."""
        return self['authority_name']

    def classes(self, class_name_or_id: Optional[str] = None) -> Union[ClassesGroup, ClassificationSystemClass]:
        """:return: classes of the classification system."""
        _classes_data = next(Utils._get(link['href']) for link in self['links'] if link['rel'] == 'classes')

        if class_name_or_id is not None:
            _classes_link = [link['href'] for link in self['links'] if link['rel'] == 'classes'][0]
            link = _classes_link.split('classes')
            data = Utils._get(f'{link[0]}classes/{class_name_or_id}{link[1]}')
            return ClassificationSystemClass(data, self._validate)

        all_classes = ClassesGroup(dict(classes=_classes_data))
        return all_classes.classes

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('classification_system.html', classification_system=self)

    def __repr__(self) -> str:
        """Return the string representation of a classification system object."""
        text = f'{self.id}:{self.name}-{self.version} - Title: {self.title}'
        return text

    def __str__(self) -> str:
        """Return the string representation of a classification system object."""
        return f'<Classification System [{self.id}:{self.name}-{self.version} - Title: {self.title}]>'


