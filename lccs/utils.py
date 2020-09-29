#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Client Library for the LCCS Web Service."""
import re
import requests

from jsonschema import RefResolver, validate
from pkg_resources import resource_filename

base_schemas_path = resource_filename(__name__, 'jsonschemas/')

class Utils:
    """Utils class."""

    @staticmethod
    def _get(url, params=None):
        """Query the LCCS-WS using HTTP GET verb and return the result as a JSON document.

        :param url: The URL to query must be a valid LCCS-WS endpoint.
        :type url: str

        :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the underlying `Requests`.
        :type params: dict

        :rtype: dict
        :raises ValueError: If the response body does not contain a valid json.
        """
        response = requests.get(url, params=params)

        response.raise_for_status()

        content_type = response.headers.get('content-type')

        if content_type == 'application/octet-stream':

            content = response.headers.get('content-disposition')

            try:
                file_name = re.findall('filename=(.+)', content)[0]
            except:
                raise ValueError('Error while download file')

            return file_name, response.content

        elif content_type not in ('application/json', 'application/geo+json'):
            raise ValueError('HTTP response is not JSON: Content-Type: {}'.format(content_type))

        return response.json()

    @staticmethod
    def validate(lccs_object):
        """Validate a lucc Object using its jsonschemas.

        :raise ValidationError: raise a ValidationError if the lucc Object couldn't be validated.
        """
        resolver = RefResolver("file://{}{}/".format(base_schemas_path, lccs_object))

        validate(lccs_object, lccs_object._schema, resolver=resolver)
