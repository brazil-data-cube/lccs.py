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
import enum
import json
from pathlib import Path
from typing import Any

from cachetools import LRUCache, cached

from .classification_system import ClassificationSystem
from .mappings import MappingGroup
from .style_formats import StyleFormats
from .style_utils import SldGenerator
from .utils import Utils


class LCCS:
    """This class implements a Python API client wrapper for LCCS-WS.

    See https://github.com/brazil-data-cube/lccs-ws for more
    information on LCCS-WS.

    :param url: The LCCS-WS server URL.
    :type url: str
    """

    _url: str
    _validate: bool
    _access_token: str | None
    _support_l: enum.EnumMeta
    _language: str | None
    _classification_systems: list[dict[str, str]]

    def __init__(self, url: str, validate=False, access_token=None, language=None):
        """Create a LCCS-WS client attached to the given host address (an URL)."""
        self._url = url.rstrip("/")
        self._validate = validate
        self._access_token = access_token if access_token else ""
        self._support_l = self._support_language()
        self._language = (
            self._validate_language(language) if language else None
        )  # Apenas o código, ex: 'en'
        self._classification_systems = self._get_classification_systems()

    def _support_language(self):
        """Get the support language from service."""
        import enum

        data = Utils._get(f"{self._url}/", access_token=self._access_token)
        return enum.Enum(
            "Language",
            {i["language"]: i["language"] for i in data["supported_language"]},
            type=str,
        )

    def _validate_language(self, language):
        """Validate and return language code."""
        if language in [e.value for e in self._support_l]:
            return language
        else:
            s = ", ".join(self.allowed_language)
            raise KeyError(f"Language not supported! Use: {s}")

    def _get_format_identifier(self, name):
        url = f"{self._url}/style_formats/search/{name}"
        data = Utils._get(url)
        return data

    def _get_classification_systems(self):
        """Return the Classification Systems available in service."""
        url = f"{self._url}/classification_systems"
        params = {"language": self._language} if self._language else None
        data = Utils._get(url, access_token=self._access_token, params=params)
        result = []
        for i in data:
            result.append(
                dict(identifier=i["identifier"], title=i["title"], version=i["version"])
            )
        return result

    def _id(self, system_name: str):
        for k, v in self._classification_systems[0].items():
            if k == system_name:
                return v
        return None

    def _name(self, system_id: int):
        for k, v in self._classification_systems[0].items():
            if v.id == int(system_id):
                return k
        return None

    @property
    def allowed_language(self):
        """Retrieve a list of languages allowed by the service."""
        return [e.value for e in self._support_l]

    @property
    def classification_systems(self):
        """Retrieve the list of names of all available classification systems in the service.

        :returns: list of Classification Systems.
        :rtype: dict
        """
        return self._classification_systems

    @cached(cache=LRUCache(maxsize=128))
    def classification_system(self, system: str) -> ClassificationSystem:
        """Return information about the given classification system.

        :param system: A str with name-version for a given classification_system.
        :type system: str

        :returns: A ClassificationSystem.
        :rtype: dict
        """
        url = f"{self._url}/classification_systems/{system}"
        params = {"language": self._language} if self._language else None
        try:
            data = Utils._get(url, access_token=self._access_token, params=params)
            return ClassificationSystem(
                data, self._validate
            )  # pyright: ignore[reportArgumentType]
        except Exception as exc:
            raise KeyError(
                f"Could not retrieve information for classification_system: {system}"
            ) from exc

    @cached(cache=LRUCache(maxsize=128))
    def available_mappings(self, system_source: str) -> list:
        """Return the available mappings of classification system.

        :param system_source: The name or identifier of classification system.
        :type system_source: str

        :returns: Available Classification Systems Mappings.
        :rtype: list
        """
        url = f"{self._url}/mappings/{system_source}"
        params = {"language": self._language} if self._language else None
        try:
            data = Utils._get(url, access_token=self._access_token, params=params)
        except Exception:
            raise KeyError(
                f"Could not retrieve any available mapping for {system_source}"
            )

        result = []
        for i in data:
            if i["rel"] == "child":
                system_target = self.classification_system(
                    i["href"].split("/")[-1].split("?")[0]
                )
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
        url = f"{self._url}/mappings/{system_source}/{system_target}"
        try:
            data = Utils._get(url, access_token=self._access_token)
        except Exception:
            raise KeyError(
                f"Could not retrieve mappings for {system_source} and {system_target}"
            )

        data_result = {"mappings": data}
        return MappingGroup(data_result, self._validate)

    def available_style_formats(self) -> list:
        """Fetch the available style formats.

        :returns: Available style formats.
        :rtype: list
        """
        result = []
        try:
            data = Utils._get(
                f"{self._url}/style_formats", access_token=self._access_token
            )
        except Exception:
            raise KeyError("Could not retrieve any style format")

        for i in data:
            for links in i["links"]:
                if links["rel"] == "items":
                    data = Utils._get(
                        f"{links['href']}", access_token=self._access_token
                    )
                    result.append(StyleFormats(data))

        return result

    @cached(cache=LRUCache(maxsize=128))
    def style_formats(self, system) -> list[StyleFormats]:
        """Fetch styles of the a giving classification system.

        :param system: The id or identifier of a classification system.
        :type system: str

        :returns: Available Classification Systems Styles.
        :rtype: list
        """
        result = []
        try:
            data = Utils._get(
                f"{self._url}/classification_systems/{system}/style_formats",
                access_token=self._access_token,
            )
        except Exception:
            raise KeyError(f"Could not retrieve any style format for {system}")

        for i in data:
            if i["rel"] == "style":
                style_id = i["href"].split("/")[-1]
                style_data = Utils._get(
                    f"{self._url}/style_formats/{style_id}",
                    access_token=self._access_token,
                )
                result.append(StyleFormats(style_data))

        return result

    # TODO
    def get_style(self, system, style_format, path=None):
        """Fetch styles of a giving classification system.

        :param system: The id or identifier of a classification system.
        :type system: str

        :param style_format: The id or name of style format.
        :type style_format: str

        :param path: Directory path to save the file
        :type path: str

        :returns: Style
        :rtype: File
        """
        try:
            file_name, data = Utils._get(
                f"{self._url}/classification_systems/{system}/styles/{style_format}",
                access_token=self._access_token,
            )
        except Exception:
            raise KeyError(f"Could not retrieve any style for {system}")

        if path is not None:
            full_path = path + file_name
            return open(full_path, "wb").write(data)
        return open(file_name, "wb").write(data)

    def add_classification_system(self, system_path: str | dict) -> list[dict]:
        """Add new classification system."""
        url = f"{self._url}/classification_systems"

        if type(system_path) == str:
            with open(system_path, encoding="utf-8") as file:
                system_path = json.load(file)
        try:
            retval = Utils._post(url, access_token=self._access_token, json=system_path)

        except RuntimeError:
            raise ValueError("Could not insert classes!")

        return retval

    def update_class(self, system: str, class_id: int, class_info: dict) -> list[dict]:
        """Update class to a classification system."""
        url = f"{self._url}/classification_systems/{system}/classes/{class_id}"

        try:
            retval = Utils._put(url, access_token=self._access_token, json=class_info)
        except RuntimeError:
            raise ValueError("Could not update class!")

        return retval

    def add_classes(
        self, system: str, classes: str | list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Add new classes to an classification system."""
        url = f"{self._url}/classification_systems/{system}/classes"

        if isinstance(classes, str):
            classes_path = Path(classes)
            if not classes_path.exists():
                raise ValueError(f"File not found: {classes_path}")

            try:
                with classes_path.open("r", encoding="utf-8") as f:
                    classes = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON file: {classes_path}") from exc

        for i in classes:  # type: dict[str, Any]
            if "class_parent_id" not in i:
                break
            if not isinstance(i["class_parent_id"], str):
                break
            i["class_parent_id"] = Utils.get_id_by_name(
                name=i["class_parent_id"], classes=_system_id.classes
            )

        try:
            retval = Utils._post(url=url, access_token=self._access_token, json=classes)

        except RuntimeError:
            raise ValueError("Could not insert classes!")

        return retval

    def add_style(
        self,
        system: str,
        style_format: str,
        style_path: str = None,
        style_tex: str = None,
        style_name: str = None,
        style_extension: str = None,
    ) -> list[dict]:
        """Add a new style to a system."""
        url = f"{self._url}/classification_systems/{system}/styles"

        if style_path:
            try:
                style = {"style": open(style_path, "rb")}
            except RuntimeError:
                raise ValueError(f"Could not open style file {style_path}.")
        elif style_tex:
            style = {"style": (f"{style_name}.{style_extension}", f"{style_tex}")}
        else:
            raise ValueError("You must provide a file path or a string with the style!")

        data = dict(style_format=style_format)

        try:
            retval = Utils._post(
                url, access_token=self._access_token, data=data, files=style
            )
        except RuntimeError:
            raise ValueError("Could not insert style!")

        return retval

    def add_mapping(self, system_source: str, system_target: str, mappings) -> list:
        """Add new classification system mapping."""
        url = f"{self._url}/mappings/{system_source}/{system_target}"

        if type(mappings) == str:
            with open(mappings, encoding="utf-8") as file:
                mappings = json.load(file)
        try:
            retval = Utils._post(url, access_token=self._access_token, json=mappings)
        except RuntimeError:
            raise ValueError("Could not insert mappings!")

        return retval

    def add_style_format(self, name: str) -> dict:
        """Add a new style format."""
        url = f"{self._url}/style_formats"

        data = {"name": name}

        try:
            retval = Utils._post(url, access_token=self._access_token, json=data)
        except RuntimeError:
            raise ValueError(f"Could not insert style format {name}!")

        return retval

    def delete_classification_system(self, system: str) -> int:
        """Delete a specific classification system."""
        try:
            retval = Utils._delete(
                f"{self._url}/classification_systems/{system}",
                access_token=self._access_token,
            )
        except RuntimeError:
            raise ValueError(f"Could not remove classification system {system}!")

        return retval.status_code

    def delete_class(self, system: str, class_name_or_id: str) -> int:
        """Delete a specific class."""
        try:
            retval = Utils._delete(
                f"{self._url}/classification_systems/{system}/classes/{class_name_or_id}",
                access_token=self._access_token,
            )
        except RuntimeError:
            raise ValueError(
                f"Could not remove class {class_name_or_id} of classification system {system}!"
            )

        return retval.status_code

    def delete_style_format(self, style_format: str) -> int:
        """Delete a specific style format."""
        try:
            retval = Utils._delete(
                f"{self._url}/style_formats/{style_format}",
                access_token=self._access_token,
            )
        except RuntimeError:
            raise ValueError(f"Could not remove style format {style_format} !")

        return retval.status_code

    def delete_style(self, system: str, style_format: str) -> int:
        """Delete the style of a classification system."""
        try:
            retval = Utils._delete(
                f"{self._url}/classification_systems/{system}/styles/{style_format}",
                access_token=self._access_token,
            )
        except RuntimeError:
            raise ValueError(
                f"Could not remove style {style_format} of classification system {system}!"
            )

        return retval.status_code

    def delete_mapping(self, system_source: str, system_target: str) -> int:
        """Delete the mapping."""
        try:
            retval = Utils._delete(
                f"{self._url}/mappings/{system_source}/{system_target}",
                access_token=self._access_token,
            )
        except RuntimeError:
            raise ValueError(
                f"Could not remove mapping of {system_source} and {system_target}!"
            )

        return retval.status_code

    def create_style(self, system: str, style_format: str, options: dict, rules: list):
        """Create style sld."""
        sld = SldGenerator.create_sld(options=options, rules=rules, layer_name=system)

        self.add_style(
            system=system,
            style_format=style_format,
            style_tex=sld.decode("utf-8"),
            style_name="lccs-style",
            style_extension="sld",
        )

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
        return f"<LCCS [{self.url}]>"

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html(
            "classification_systems.html",
            classification_systems=self.classification_systems,
        )
