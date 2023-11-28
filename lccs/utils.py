#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Python Client Library for the LCCS Web Service."""
import re
import requests
import jinja2

from jsonschema import RefResolver, validate
from pkg_resources import resource_filename

base_schemas_path = resource_filename(__name__, 'jsonschemas/')
templateLoader = jinja2.FileSystemLoader(searchpath=resource_filename(__name__, 'templates/'))
templateEnv = jinja2.Environment(loader=templateLoader)


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
            except RuntimeError:
                raise ValueError('Error while download file')

            return file_name, response.content

        elif content_type not in ('application/json', 'application/geo+json'):
            raise ValueError('HTTP response is not JSON: Content-Type: {}'.format(content_type))

        return response.json()

    @staticmethod
    def _post(url, data=None, json=None, files=None):
        """Request post method."""
        response = requests.post(url, data=data, files=files, json=json)

        response.raise_for_status()

        return response.json()

    @staticmethod
    def _delete(url, params=None):
        """Request delete method."""
        response = requests.delete(url, params=params)

        response.raise_for_status()

        return response

    @staticmethod
    def validate(lccs_object):
        """Validate a lucc Object using its jsonschemas.

        :raise ValidationError: raise a ValidationError if the lucc Object couldn't be validated.
        """
        resolver = RefResolver("file://{}{}/".format(base_schemas_path, lccs_object))

        validate(lccs_object, lccs_object._schema, resolver=resolver)

    @staticmethod
    def render_html(template_name, **kwargs):
        """Render Jinja2 HTML template."""
        template = templateEnv.get_template(template_name)
        return template.render(**kwargs)

    @staticmethod
    def get_id_by_name(name, classes):
        """Get id of class."""
        return list(filter(lambda x: x.name == name, classes))[0]['id']
