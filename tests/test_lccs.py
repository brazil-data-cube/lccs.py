#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service. is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for Python Client Library for the LCCS Web Service operations."""

import os

import lccs

url =  os.environ.get('LCCS_SERVER_URL', 'http://localhost:5000/lccs')

class TestLCCS:
    def test_lccs(self):
        service = lccs.lccs(url)
        assert service.url == url
        assert repr(service) == 'lccs("{}")'.format(url)
        assert str(service) == '<LCCS [{}]>'.format(url)
