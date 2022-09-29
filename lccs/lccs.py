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
"""Python API client wrapper for LCCS-WS."""
from typing import List
from .classification_system import ClassificationSystem
from .mappings import MappingGroup, Mapping
from .style_formats import StyleFormats
from .utils import Utils
from .style_utils import SldGenerator
import json

from cachetools import cached, LRUCache


class LCCS:
    """This class implements a Python API client wrapper for LCCS-WS.

    See https://github.com/brazil-data-cube/lccs-ws for more
    information on LCCS-WS.

    :param url: The LCCS-WS server URL.
    :type url: str
    """

    def __init__(self, url, validate=False, access_token=None, language=None):
        """Create a LCCS-WS client attached to the given host address (an URL)."""
        self._url = url.rstrip('/')
        self._validate = validate
        self._classification_systems = {}
        self._access_token = f'?access_token={access_token}' if access_token else ''
        self._support_l = self._support_language()
        self._language = self._validate_language(language) if language else ''

    def _support_language(self):
        """Get the support language from service."""
        import enum
        data = Utils._get(f'{self._url}/')
        return enum.Enum('Language', {i['language']: i['language'] for i in data['supported_language']}, type=str)

    def _validate_language(self, language):
        """Get the support language from service."""
        if language in [e.value for e in self._support_l]:
            return f'&language={language}'
        else:
            s = ', '.join([e for e in self.allowed_language])
            raise KeyError(f'Language not supported! Use: {s}')

    def _get_format_identifier(self, name):
        url = f'{self._url}/style_formats/search/{name}'
        data = Utils._get(url)
        return data

    def _get_classification_systems(self):
        """Return the Classification Systems available in service."""
        url = f'{self._url}/classification_systems{self._access_token}{self._language}'
        data = Utils._get(url)
        result = list()

        [result.append(i['identifier']) for i in data]

        return result

    def _id(self, system_name: str):
        for k, v in self._classification_systems.items():
            if k == system_name:
                return v

    def _name(self, system_id: int):
        for k, v in self._classification_systems.items():
            if v.id == int(system_id):
                return k

    @property
    def allowed_language(self):
        """Retrieve a list of languages allowed by the service."""
        return [e.value for e in self._support_l]

    @property
    def classification_systems(self):
        """Retrieve the list of names of all available classification systems in the service.

        :returns: List of Classification Systems.
        :rtype: dict
        """
        return self._get_classification_systems()

    @cached(cache=LRUCache(maxsize=128))
    def classification_system(self, system: str) -> ClassificationSystem:
        """Return information about the given classification system.

        :param system: A str with name-version for a given classification_system.
        :type system: str

        :returns: A ClassificationSystem.
        :rtype: dict
        """
        try:
            url = f'{self._url}/classification_systems/{system}{self._access_token}{self._language}'
            data = Utils._get(url)
            return ClassificationSystem(data, self._validate)
        except Exception:
            raise KeyError(f'Could not retrieve information for classification_system: {system}')

    @cached(cache=LRUCache(maxsize=128))
    def available_mappings(self, system_source: str) -> list:
        """Return the available mappings of classification system.

        :param system_source: The name or identifier of classification system.
        :type system_source: str

        :returns: Available Classification Systems Mappings.
        :rtype: list
        """
        result = list()

        try:
            data = Utils._get(f'{self._url}/mappings/{system_source}{self._access_token}{self._language}')
        except Exception:
            raise KeyError(f'Could not retrieve any available mapping for {system_source}')

        for i in data:
            if i['rel'] == 'child':
                system_target = self.classification_system(i['href'].split("/")[-1].split('?')[0])
                result.append(system_target)

        return result

    @cached(cache=LRUCache(maxsize=128))
    def mappings(self, system_source: str, system_target: str) -> MappingGroup:
        """Return the given classification_system.

        :param system_source: The name or identifier of classification system.
        :type system_source: str
        :param system_target: The name or identifier of classification system.
        :type system_target: str

        :returns: Mappings of classification Systems.
        :rtype: list
        """
        try:
            data = Utils._get(f'{self._url}/mappings/{system_source}/{system_target}{self._access_token}')
        except Exception:
            raise KeyError(f'Could not retrieve mappings for {system_source} and {system_target}')

        data_result = dict()
        data_result['mappings'] = data

        return MappingGroup(data_result, self._validate)

    def available_style_formats(self) -> list:
        """Fetch the available style formats.

        :returns: Available style formats.
        :rtype: list
        """
        result = list()

        try:
            data = Utils._get(f'{self._url}/style_formats{self._access_token}')
        except Exception:
            raise KeyError('Could not retrieve any style format')

        for i in data:
            for links in i['links']:
                if links['rel'] == 'items':
                    data = Utils._get(f"{links['href']}")
                    result.append(StyleFormats(data))

        return result

    @cached(cache=LRUCache(maxsize=128))
    def style_formats(self, system) -> List[StyleFormats]:
        """Fetch styles of the a giving classification system.

        :param system: The id or identifier of a classification system.
        :type system: str

        :returns: Available Classification Systems Styles.
        :rtype: list
        """
        result = list()
        try:
            data = Utils._get(f'{self._url}/classification_systems/{system}/style_formats{self._access_token}')
        except Exception:
            raise KeyError(f'Could not retrieve any style format for {system}')
        for i in data:
            if i['rel'] == 'style':
                data = Utils._get(f'{self._url}/style_formats/{i["href"].split("/")[-1]}')
                result.append(StyleFormats(data))

        return result

    #TODO
    def get_style(self, system, style_format, path=None):
        """Fetch styles of the a giving classification system.

        :param system: The id or identifier of a classification system.
        :type system: str

        :param style_format: The id or name of style format.
        :type style_format: str

        :param path: Directory path to save the file
        :type path: str

        :returns: Style File
        :rtype: File
        """
        try:
            file_name, data = Utils._get(f'{self._url}/classification_systems/{system}/styles/{style_format}{self._access_token}')
        except Exception:
            raise KeyError(f'Could not retrieve any style for {system}')

        if path is not None:
            full_path = path + file_name
            return open(full_path, 'wb').write(data)
        return open(file_name, 'wb').write(data)

    def add_classification_system(self, name: str, authority_name: str, description: dict, title: dict,
                                  version: str) -> dict:
        """Add a new classification system."""
        url = f'{self._url}/classification_systems{self._access_token}'

        data = dict()
        data["name"] = name
        data["authority_name"] = authority_name
        data["version"] = version
        data["description"] = description
        data["title"] = title

        try:
            retval = Utils._post(url, json=data)
        except RuntimeError as e:
            raise ValueError(f'Could not insert classification system {name}!')

        return retval

    def add_classes(self, system: str, classes: str) -> List[dict]:
        """Add new classes to an classification system."""
        url = f'{self._url}/classification_systems/{system}/classes{self._access_token}'

        if type(classes) == str:
            with open(classes) as file:
                classes = json.load(file)

        try:
            retval = Utils._post(url, json=classes)
        except RuntimeError:
            raise ValueError('Could not insert classes!')

        return retval

    def add_style(self, system: str, style_format: str, style_path: str = None, style_tex: str = None,
                  style_name: str = None, style_extension: str = None) -> List[dict]:
        """Add a new style to a system."""
        url = f'{self._url}/classification_systems/{system}/styles{self._access_token}'

        if style_path:
            try:
                style = {'style': open(style_path, 'rb')}
            except RuntimeError:
                raise ValueError(f'Could not open style file {style_path}.')
        elif style_tex:
            style = {'style': (f'{style_name}.{style_extension}', f'{style_tex}')}
        else:
            raise ValueError('You must provide a file path or a string with the style!')

        data = dict(style_format=style_format)

        try:
            retval = Utils._post(url, data=data, files=style)
        except RuntimeError:
            raise ValueError('Could not insert style!')

        return retval

    def add_mapping(self, system_source: str, system_target: str, mappings) -> list:
        """Add new classification system mapping."""
        url = f'{self._url}/mappings/{system_source}/{system_target}{self._access_token}'

        if type(mappings) == str:
            with open(mappings) as file:
                mappings = json.load(file)
        try:
            retval = Utils._post(url, json=mappings)
        except RuntimeError:
            raise ValueError('Could not insert mappings!')

        return retval

    def add_style_format(self, name: str) -> dict:
        """Add a new style format."""
        url = f'{self._url}/style_formats{self._access_token}'

        data = {"name": name}

        try:
            retval = Utils._post(url, json=data)
        except RuntimeError:
            raise ValueError(f'Could not insert style format {name}!')

        return retval

    def delete_classification_system(self, system: str) -> int:
        """Delete a specific classification system."""
        try:
            retval = Utils._delete(f'{self._url}/classification_systems/{system}{self._access_token}')
        except RuntimeError:
            raise ValueError(f'Could not remove classification system {system}!')

        return retval.status_code

    def delete_class(self, system: str, class_name_or_id: str) -> int:
        """Delete a specific class."""
        try:
            retval = Utils._delete(f'{self._url}/classification_systems/{system}/classes/{class_name_or_id}{self._access_token}')
        except RuntimeError:
            raise ValueError(f'Could not remove class {class_name_or_id} of classification system {system}!')

        return retval.status_code

    def delete_style_format(self, style_format: str) -> int:
        """Delete a specific style format."""
        try:
            retval = Utils._delete(f'{self._url}/style_formats/{style_format}{self._access_token}')
        except RuntimeError:
            raise ValueError(f'Could not remove style format {style_format} !')

        return retval.status_code

    def delete_style(self, system: str, style_format: str) -> int:
        """Delete the style of a classification system."""
        try:
            retval = Utils._delete(f'{self._url}/classification_systems/{system}/styles/{style_format}{self._access_token}')
        except RuntimeError:
            raise ValueError(f'Could not remove style {style_format} of classification system {system}!')

        return retval.status_code

    def delete_mapping(self, system_source: str, system_target: str) -> int:
        """Delete the mapping."""
        try:
            retval = Utils._delete(f'{self._url}/mappings/{system_source}/{system_target}{self._access_token}')
        except RuntimeError:
            raise ValueError(f'Could not remove mapping of {system_source} and {system_target}!')

        return retval.status_code

    #TODO
    def create_style(self, system: str, style_format: str, options: dict, rules: list):
        """Create style sld."""
        sld = SldGenerator.create_sld(options=options, rules=rules, layer_name=system)

        self.add_style(system=system, style_format=style_format, style_tex=sld.decode("utf-8"), style_name='lccs-style', style_extension='sld')

        return

    @property
    def url(self):
        """Return the LCSS server instance URL."""
        return self._url

    def __repr__(self):
        """Return the string representation of a lccs object."""
        text = f'lccs("{self.url}")'
        return text

    def __str__(self):
        """Return the string representation of a lccs object."""
        return f'<LCCS [{self.url}]>'

    def _repr_html_(self):
        """HTML repr."""
        classification_systems = str()
        for classification_sys in self.classification_systems:
            classification_systems += f"<li>{classification_sys}</li>"
        return f"""<p>LCCS-WS</p>
                    <ul>
                     <li><b>URL:</b> {self._url}</li>
                     <li><b>Classification Systems:</b></li>
                     <ul>
                     {classification_systems}
                     </ul>
                   </ul>
               """
