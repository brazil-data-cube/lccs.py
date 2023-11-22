#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service. is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for Python Client Library for the LCCS Web Service operations."""

import json
import os
import re
from pathlib import Path

import pytest
from pkg_resources import resource_filename, resource_string

import lccs

url = os.environ.get('LCCS_SERVER_URL', 'http://localhost:5000')

match_url = re.compile(url)
match_url_system = re.compile(url + '/1')
match_url_class = re.compile(url + '/1/classes')
match_url_mappings = re.compile(url + '/mappings')


@pytest.fixture(scope='session')
def lccs_object():
    resource_package = __name__
    directory = resource_filename(resource_package, 'jsons/')
    files = dict()
    for path in Path(directory).rglob('*.json'):
        path = str(path)

        s = path.split('/')

        file_path = '/'.join(s[-2:])

        file = json.loads(resource_string(resource_package, file_path).decode('utf-8'))

        if s[-2] in files:
            files[s[-2]][s[-1]] = file
        else:
            files[s[-2]] = {s[-1]: file}

    return files


class TestLCCS:
    
    def _setup_lccs(self, mock, json_systems=None, json_class=None, json_system=None, json_mappings=None):
        if json_systems is not None:
            mock.get(match_url, json=json_systems,
                     status_code=200,
                     headers={'content-type': 'application/json'})
        if json_system is not None:
            mock.get(match_url_system, json=json_system,
                     status_code=200,
                     headers={'content-type': 'application/json'})
        if json_class is not None:
            mock.get(match_url_class, json=json_class,
                     status_code=200,
                     headers={'content-type': 'application/json'})
        if json_mappings is not None:
            mock.get(match_url_mappings, json=json_mappings,
                     status_code=200,
                     headers={'content-type': 'application/json'})

    def test_lccs(self, requests_mock):
        requests_mock.get(match_url, json=dict(version='0.8.2',
                                               application_name="Land Cover Classification System Service",
                                               links=list(),
                                               supported_language=list([dict(language="pt-br",
                                                                             description="Brazilian Portuguese")])),
                          status_code=200,
                          headers={'content-type': 'application/json'})

        self._setup_lccs(requests_mock, list(), list())

        service = lccs.LCCS(url)
        assert service.url == url
        assert repr(service) == 'lccs("{}")'.format(url)
        assert str(service) == '<LCCS [{}]>'.format(url)

    def test_classification_systems(self, lccs_object, requests_mock):
        for k in lccs_object:
            self._setup_lccs(requests_mock, json_systems=lccs_object[k]['classification_systems.json'],
                             json_class=lccs_object[k]['classes.json'])

            service = lccs.LCCS(url, True)

            response = service.classification_systems

            assert response == ['prodes-1.0']

    def test_classification_system(self, lccs_object, requests_mock):
        for k in lccs_object:
            self._setup_lccs(requests_mock, json_systems=lccs_object[k]['classification_systems.json'],
                             json_class=lccs_object[k]['classes.json'],
                             json_system=lccs_object[k]['classification_system.json'])

            service = lccs.LCCS(url, True)

            class_system = service.classification_system('prodes-1.0')

            assert class_system.id
            assert class_system.name
            assert class_system.title
            assert class_system.identifier
            assert class_system.description
            assert class_system.version
            assert class_system.links[0].href
            assert class_system.links[0].rel


if __name__ == '__main__':
    pytest.main(['--color=auto', '--no-cov'])
