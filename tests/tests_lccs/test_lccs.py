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
import respx
from httpx import Response

import lccs

url = os.environ.get("LCCS_SERVER_URL", "http://localhost:5000")

match_url = re.compile(url + "/")
match_url_systems = re.compile(url + "/classification_systems")
match_url_system = re.compile(url + "/classification_systems/1")
match_url_class = re.compile(url + "/classification_systems/1/classes")
match_url_mappings = re.compile(url + "/mappings/1")


@pytest.fixture(scope="session")
def lccs_object():
    """Load jsons files."""
    base_dir = Path(__file__).parent / "jsons"
    files = {}
    for path in base_dir.rglob("*.json"):
        rel_parts = path.parts[-2:]  # pega última pasta + arquivo
        folder, filename = rel_parts
        with open(path, encoding="utf-8") as f:
            file_data = json.load(f)
        files.setdefault(folder, {})[filename] = file_data
    return files


class TestLCCS:

    def _setup_lccs(
        self,
        root=None,
        json_systems=None,
        json_class=None,
        json_system=None,
        json_mappings=None,
    ):
        """Config mocks endpoints."""
        if root is not None:
            respx.get(match_url).mock(return_value=Response(200, json=root))
        if json_systems is not None:
            respx.get(match_url_systems).mock(
                return_value=Response(200, json=json_systems)
            )
        if json_system is not None:
            respx.get(match_url_system).mock(
                return_value=Response(200, json=json_system)
            )
        if json_class is not None:
            respx.get(match_url_class).mock(return_value=Response(200, json=json_class))
        if json_mappings is not None:
            respx.get(match_url_mappings).mock(
                return_value=Response(200, json=json_mappings)
            )

    @respx.mock
    def test_lccs(self, lccs_object):
        respx.get(match_url).mock(
            return_value=Response(
                200,
                json=dict(
                    lccs_version="1.0.1",
                    links=[],
                    application_name="Land Cover Classification System Service",
                    supported_language=[
                        dict(language="pt-br", description="Brazilian Portuguese")
                    ],
                ),
            )
        )

        for k in lccs_object:
            self._setup_lccs(root=lccs_object[k].get("root.json"))

        service = lccs.LCCS(url)

        assert service.url == url
        assert repr(service) == f'lccs("{url}")'
        assert str(service) == f"<LCCS [{url}]>"
