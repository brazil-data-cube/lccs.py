#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
from .link import Link


class StyleFormats(dict):
    """Class."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with style format metadata.

        :param validate: true if the style format should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(StyleFormats, self).__init__(data or {})

    @property
    def id(self):
        """:return: the style format id."""
        return self['id']

    @property
    def name(self):
        """:return: the style format name."""
        return self['name']
    
    @property
    def links(self):
        """:return: a list of link in the classification system."""
        return [Link(link) for link in self['links']]
    
    def __repr__(self):
        """Return the string representation of a style format object."""
        text = f'Name:{self.name}'
        return text

    def __str__(self):
        """Return the string representation of a style format object."""
        return f'<Name:{self.name}>'


