#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2019 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for LCCS-WS."""

from .class_system import ClassificationSystem
from .mappings import Mappings
from .utils import Utils


class lccs:
    """This class implements a Python API client wrapper for LCCS-WS.

    See https://github.com/brazil-data-cube/lccs-ws for more
    information on LCCS-WS.

    :param url: The LCCS-WS server URL.
    :type url: str
    """

    def __init__(self, url, validate=False):
        """Create a LCCS-WS client attached to the given host address (an URL)."""
        self._url = url if url[-1] != '/' else url[0:-1]
        self._classification_systems = {}
        self._validate = validate

    @property
    def get_classification_systems(self):
        """Return the Classification Systems avaliable in service."""
        if len(self._classification_systems) > 0:
            return self._classification_systems.keys()

        url = '{}/classification_systems'.format(self._url)

        for i in (ClassificationSystem(Utils._get(url), self._validate)).links:
            if i.rel == 'child':
                self._classification_systems[i.href.split('/')[-1]] = None

        return self._classification_systems.keys()

    @property
    def classification_systems(self):
        """Retrieve the list of names of all available classification systems in the service.

        :returns: List of Classification Systems.
        :rtype: dict
        """
        if self.get_classification_systems:
            pass
        return self._classification_systems.keys()

    def classification_system(self, system_id):
        """Return information about the given classification system.

        :param system_id: A str for a given classification_systems_id.
        :type system_id: str

        :returns: A ClassificationSystem.
        :rtype: dict
        """
        if system_id in self._classification_systems.keys() and self._classification_systems[system_id] is not None:
            return self._classification_systems[system_id]
        try:
            data = Utils._get('{}/classification_systems/{}'.format(self._url, system_id))
            self._classification_systems[system_id] = ClassificationSystem(data, self._validate)
        except Exception:
            raise KeyError('Could not retrieve information for classification_system: {}'.format(system_id))
        return self._classification_systems[system_id]

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

    def avaliable_mappings(self, system_id_source):
        """Return the avaliable mappings of classification system.

        :param system_id_source: A str for a given system_id_source.
        :type system_id_source: str

        :returns: Avaliable Classification Systems Mappings.
        :rtype: list
        """
        result = list()

        try:
            data = Utils._get('{}/mappings/{}'.format(self._url, system_id_source))
        except Exception:
            raise KeyError('Could not retrieve any avaliable mapping for {}'.format(system_id_source))

        [result.append(i['rel']) for i in data]

        return result

    def styles(self, system_id):
        """Fetch styles of the a giving classification system.

        :param system_id: A classification System system_id (name).
        :type system_id: str

        :returns: Avaliable Classification Systems Styles.
        :rtype: list
        """
        try:
            data = Utils._get('{}/classification_systems/{}/styles'.format(self._url, system_id))
            return data
        except Exception:
            raise KeyError('Could not retrieve any style for {}'.format(system_id))



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
