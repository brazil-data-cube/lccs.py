#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""


class ClassificationSystemClass(dict):
    """Class of the classification system."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Class metadata.

        :param validate: true if the Class should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(ClassificationSystemClass, self).__init__(data or {})

    @property
    def id(self):
        """:return: the class id."""
        return self['id']

    @property
    def description(self):
        """:return: the class description."""
        return self['description']

    @property
    def name(self):
        """:return: the class name."""
        return self['name']

    @property
    def code(self):
        """:return: the class code."""
        return self['code']

    @property
    def class_parent_id(self):
        """:return: the class parent id."""
        return self['class_parent_id'] if 'class_parent_id' in self else None

    @property
    def class_parent_name(self):
        """:return: the class parent name."""
        return self['class_parent_name'] if 'class_parent_name' in self else None
