#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
from .class_system import ClassSystemClass
from .utils import Utils


class Mappings(dict):
    """Mappings."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Classes metadata.
        :param validate: true if the Classes should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(Mappings, self).__init__(data or {})

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
        for i in self['links']:
            if i['rel'] == 'source_class':
                return ClassSystemClass(Utils._get(i['href'], self._validate))

    @property
    def target_class(self):
        """:return: the Class code."""
        for i in self['links']:
            if i['rel'] == 'target_class':
                return ClassSystemClass(Utils._get(i['href'], self._validate))
