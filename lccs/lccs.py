#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2019 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for LCCS-WS."""

from .class_system import ClassSystem
from .mappings import Mappings
from .utils import Utils


class lccs:
    """This class implements a Python API client wrapper for LCCS.

    See https://github.com/brazil-data-cube/lccs-ws for more
    information on LCCS.

    :param url: The LCCS server URL.
    :type url: str
    """

    def __init__(self, url, validate=False):
        """Create a LCCS-WS client attached to the given host address (an URL)."""
        self._url = url if url[-1] != '/' else url[0:-1]
        self._class_systems = {}
        self._validate = validate

    @property
    def get_classification_systems(self):
        """Return the Classification Systems avaliable in service."""
        if len(self._class_systems) > 0:
            return self._class_systems.keys()

        url = '{}/classification_systems'.format(self._url)

        for i in (ClassSystem(Utils._get(url), self._validate)).links:
            if i.rel == 'child':
                self._class_systems[i.href.split('/')[-1]] = None

        return self._class_systems.keys()

    def classification_systems(self):
        """:return classification systems names available."""
        if self.get_classification_systems:
            pass
        return self._class_systems.keys()

    def classification_system(self, system_id):
        """Return the given classification_system.

        :param system_id: A str for a given classification_systems_id.
        :type system_id: str

        :returns: A Classification System.
        :rtype: dict
        """
        if system_id in self._class_systems.keys() and self._class_systems[system_id] is not None:
            return self._class_systems[system_id]
        try:
            data = Utils._get('{}/classification_systems/{}'.format(self._url, system_id))
            self._class_systems[system_id] = ClassSystem(data, self._validate)
        except Exception:
            raise KeyError('Could not retrieve information for classification_system: {}'.format(system_id))
        return self._class_systems[system_id]

    def mappings(self, system_id_source, system_id_target):
        """Return the given classification_system.

        :param system_id_source: A str for a given system_id_source.
        :type system_id_source: str
        :param system_id_target: A str for a given system_id_source.
        :type system_id_target: str

        :returns: Mappings of classification Systems.
        :rtype: list
        """
        result = list()
        try:
            data = Utils._get('{}/mappings/{}/{}'.format(self._url, system_id_source, system_id_target))
        except Exception:
            raise KeyError('Could not retrieve mappings for {} and {}'.format(system_id_source, system_id_target))

        [result.append(Mappings(i, self._validate)) for i in data]

        return result

    @property
    def url(self):
        """Return the LCSS server instance URL."""
        return self._url

    def __repr__(self):
        """Return the string representation of a lccs object."""
        text = 'lccs("{}")'.format(self.url)
        return text

    def __str__(self):
        """Return the string representation of a lccs object."""
        return '<LCCS [{}]>'.format(self.url)
