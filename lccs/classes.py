#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
from .utils import Utils


class ClassesGroup(dict):
    """Group of classes mappings."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Item Collection metadata.
        :param validate: true if the Item Collection should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(ClassesGroup, self).__init__(data or {})
        self._classes = [ClassificationSystemClass(i, self._validate) for i in self['classes']]

    @property
    def classes(self):
        """:return: classes."""
        return self._classes

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('mapping.html', mappings=self)

    def __repr__(self):
        """Return the string representation of a mapping group object."""
        text = ''
        for i in self._classes:
            text += f'\n\t{i}'
        return text

    def __str__(self):
        """Return the string representation of a mapping group object."""
        text = ''
        for i in self._classes:
            text += f'\n\t{i}'
        return text


class ClassificationSystemClass(dict):
    """Class of the classification system."""

    def __init__(self, data, validate=False) -> None:
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
    def name(self):
        """:return: the class name."""
        return self['name']

    @property
    def title(self):
        """:return: the class title."""
        return self['title']

    @property
    def description(self):
        """:return: the class description."""
        return self['description'] if 'description' in self else None

    @property
    def code(self):
        """:return: the class code."""
        return self['code']

    @property
    def links(self):
        """:return: the class links."""
        return self['links']

    @property
    def class_parent_id(self):
        """:return: the class parent id."""
        return self['class_parent_id'] if 'class_parent_id' in self else None

    @property
    def class_parent_name(self):
        """:return: class_parent_name of classification system."""
        return self._get_parent_name()

    def _get_parent_name(self):
        if 'class_parent_id' in self:
            parent = [link['href'] for link in self['links'] if link['rel'] == 'parent'][0]
            token = parent.rsplit('/', maxsplit=1)[1].split('?')[1]
            system = parent.rsplit('/', maxsplit=1)[1].split('?')[0]
            parent_class_uri = parent.rsplit('/', maxsplit=1)[0] + f'/{system}' + f'/classes/{self["class_parent_id"]}?{token}'
            class_parent_name = ClassificationSystemClass(Utils._get(parent_class_uri)).name
            return class_parent_name
        else:
            return None
