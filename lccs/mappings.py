#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
from .utils import Utils


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
        """:return: the Mapping."""
        return [Mapping(i, self._validate) for i in self['mappings']]

    @property
    def source_classification_system(self):
        """:return: the Class code."""
        return self['source_classification_system']

    @property
    def target_classification_system(self):
        """:return: the Class code."""
        return self['target_classification_system']

    @property
    def mapping(self):
        """:return: Classes from the class system."""
        return [Mapping(mapping, self._validate) for mapping in self['mappings']]

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('mapping.html', mappings=self)


class Mapping(dict):
    """Mapping."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Classes metadata.
        :param validate: true if the Classes should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(Mapping, self).__init__(data or {})

    @property
    def degree_of_similarity(self):
        """:return: the degree_of_similarity."""
        return self['degree_of_similarity']

    @property
    def description(self):
        """:return: the Class description."""
        return self['description']

    @property
    def link(self):
        """:return: the Class identifier (name)."""
        return self['links']

    @property
    def source_class(self):
        """:return: the Class code."""
        return self['source']

    @property
    def target_class(self):
        """:return: the Class code."""
        return self['target']
