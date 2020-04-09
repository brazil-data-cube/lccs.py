#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""

from .classes import ClassSystemClass, ClassSystemClasses
from .link import Link
from .utils import Utils


class ClassSystem(dict):
    """Classification Systems."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with class system metadata.
        :param validate: true if the Class System should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(ClassSystem, self).__init__(data or {})

    @property
    def links(self):
        """:return: a list of link in the class system."""
        return [Link(link) for link in self['links']]

    @property
    def description(self):
        """:return: description of class system."""
        return self['description']

    @property
    def name(self):
        """:return: name of class system."""
        return self['name']

    @property
    def id(self):
        """:return: id of class system."""
        return self['id']

    def classes(self, class_id=None, filter=None):
        """:return: Classes from the class system."""
        for link in self['links']:
            if link['rel'] == 'classes':
                if class_id is not None:
                    data = Utils._get('{}/{}'.format(link["href"], class_id))
                    return ClassSystemClass(data, self._validate)
                data = Utils._get(link['href'], params=filter)
                return ClassSystemClasses(data).get_class
        return ClassSystemClasses({})
