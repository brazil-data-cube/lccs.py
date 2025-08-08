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
"""LCCS Python Client examples."""

from lccs import LCCS

# Change to the LCCS-WS URL you want to use.
service = LCCS("https://data.inpe.br/bdc/lccs/v1/", access_token='change-me', language='en')

# Get a specific classification system
# Make sure the classification system is available in service
classification_system = service.classification_system('PRODES-1.0')

# Return the metadata of a specific class
class_metadata = classification_system.classes('Desmatamento')

# You can access specific attributes
print(class_metadata.id)
print(class_metadata.name)
print(class_metadata.description)
print(class_metadata.code)
