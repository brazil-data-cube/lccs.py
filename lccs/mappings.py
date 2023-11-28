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
from .utils import Utils
from .classes import ClassificationSystemClass


class MappingGroup(dict):
    """Group of classes mappings."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Item Collection metadata.
        :param validate: true if the Item Collection should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(MappingGroup, self).__init__(data or {})

    @property
    def mappings(self):
        """:return: Mapping."""
        return [Mapping(mapping, self._validate) for mapping in self['mappings']]

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('mapping.html', mappings=self)

    def __repr__(self):
        """Return the string representation of a mapping group object."""
        text = ''
        for i in self.mappings:
            text += f'\n\t{i}'
        return text

    def __str__(self):
        """Return the string representation of a mapping group object."""
        text = ''
        for i in self.mappings:
            text += f'\n\t{i}'
        return text


class Mapping(dict):
    """Mapping."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Mapping metadata.
        :param validate: true if the Classes should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(Mapping, self).__init__(data or {})
        self._source_class()
        self._target_class()

    @property
    def degree_of_similarity(self):
        """:return: the degree_of_similarity."""
        return self['degree_of_similarity']

    @property
    def description(self):
        """:return: the description."""
        return self['description']

    @property
    def link(self):
        """:return: the links."""
        return self['links']

    def _source_class(self):
        """:return: get the source_class."""
        for i in self['links']:
            if i['rel'] == 'item' and i['title'] == 'Link to source class':
                self['source_class'] = ClassificationSystemClass(Utils._get(i['href']))

    def _target_class(self):
        """:return: get the target_class."""
        for i in self['links']:
            if i['rel'] == 'item' and i['title'] == 'Link to target class':
                self['target_class'] = ClassificationSystemClass(Utils._get(i['href']))

    @property
    def source_class(self):
        """:return: the source class."""
        return self['source_class']

    @property
    def target_class(self):
        """:return: the source class."""
        return self['target_class']

    @property
    def source_class_id(self):
        """:return: the source class."""
        return self['source_class_id']

    @property
    def target_class_id(self):
        """:return: the source class."""
        return self['target_class_id']

    def __repr__(self):
        """Return the string representation of a mapping object."""
        text = f'{self.source_class.title} -> {self.target_class.title} -' \
               f' Degree_of_similarity {self.degree_of_similarity}'
        return text
    
    def __str__(self):
        """Return the string representation of a mapping object."""
        text = f'{self.source_class.title} -> {self.target_class.title} -' \
               f' Degree_of_similarity {self.degree_of_similarity}'
        return text



