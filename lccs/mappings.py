#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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
    def mapping(self):
        """:return: Mapping."""
        return [Mapping(mapping, self._validate) for mapping in self['mappings']]

    @property
    def mappings(self):
        """:return: Mappings."""
        return [Mapping(link) for link in self['links']]
    
    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('mapping.html', mappings=self)


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

    def __repr__(self):
        """Return the string representation of a mapping object."""
        text = f'{self.source_class.name} -> {self.target_class.name} -' \
               f' Degree_of_similarity {self.degree_of_similarity}'
        return text
    
    def __str__(self):
        """Return the string representation of a mapping object."""
        text = f'{self.source_class.name} -> Target Class{self.target_class.name} -' \
               f' Degree_of_similarity {self.degree_of_similarity}'
        return text



