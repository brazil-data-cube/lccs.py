#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""

from .classes import ClassificationSystemClass
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
        self['classes'] = dict()

    @property
    def links(self):
        """:return: a list of link in the classification system."""
        return [Link(link) for link in self['links']]

    @property
    def description(self):
        """:return: description of classification system."""
        return self['description']

    @property
    def version(self):
        """:return: version of classification system."""
        return self['version']

    @property
    def name(self):
        """:return: name of classification system."""
        return self['name']

    @property
    def id(self):
        """:return: id of classification system."""
        return self['id']

    @property
    def authority_name(self):
        """:return: authority_name of classification system."""
        return self['authority_name']

    def classes(self, class_name=None):
        """:return: classes of the classification system."""
        return self._get_classes(class_name)

    def _get_classes(self, class_name):
        """:return: get classes of the classification system."""
        if not bool(self['classes']):
            self._classes_links = next(Utils._get(link['href']) for link in self['links'] if link['rel'] == 'classes')

            for i in self._classes_links:
                if i['rel'] == 'child':
                    class_data = ClassificationSystemClass(Utils._get(i['href'], self._validate), self._validate)
                    if 'class_parent_id' in class_data:
                        parent_class_uri = i['href'].rsplit('/', maxsplit=1)[0] + f'/{class_data.class_parent_id}'
                        class_data['class_parent_name'] = ClassificationSystemClass(Utils._get(parent_class_uri)).name
                    self['classes'][f"{class_data.name}"] = class_data

        if class_name is not None:
            return self['classes'][f'{class_name}'] if class_name in self['classes'].keys() else {}

        return self['classes'].values()

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('classification_system.html', classification_system=self)

    def __repr__(self):
        """Return the string representation of a classification system object."""
        text = f'{self.id}:{self.name}- Version {self.version}'
        return text

    def __str__(self):
        """Return the string representation of a classification system object."""
        return f'<Classification System [{self.id}:{self.name}- Version {self.version}]>'


