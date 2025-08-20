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

import os
import lccs

print(lccs.__version__)

server_url = os.environ.get('LCCS_SERVER_URL', 'https://data.inpe.br/bdc/lccs/v1/')

service = lccs.LCCS(server_url, access_token='change-me', language='pt-br')

# The examples presented in this code vary depending on the database used. Check the parameters informed.
# Return a specific classification system
classification_system = service.classification_system('prodes-1.0')
print(classification_system.id)
print(classification_system.name)
print(classification_system.title)
print(classification_system.version)
print(classification_system.description)


# Return a classes of a classification system
classes = classification_system.classes()
print(classes)

for i in classes:
    print(f'ID: {i.id} Name: {i.name} Title: {i.title} Description :{i.description} class_parent_id {i.class_parent_id} class_parent_name {i.class_parent_name}')

# Return a specific class of a classification system
prodes_desflorestamento = classification_system.classes('1')
print(prodes_desflorestamento.title)

# Get all available mappings for a specific classification system
all_mapping = service.available_mappings(system_source='prodes-1.0')
print(all_mapping)
print(all_mapping[0].id)
print(all_mapping[0].name)
print(all_mapping[0].version)

# Get mapping
mapping = service.mappings(system_source='prodes-1.0', system_target='terraclass-amz-1.0')
print(mapping)

# Get All Styles Formarts
print(service.available_style_formats())

# Get all styles available for a specific classification system
style_formats = service.style_formats(system='prodes-1.0')
for style_f in style_formats:
    print(style_f.name)

# Save a style file of a specific classification system and style format
service.get_style(system='prodes-1.0', style_format='SLD-Feature-Polygon')

# Save Style File passing the path directory
service.get_style(system='prodes-1.0', style_format='SLD-Feature-Polygon', path='/home/user/Downloads/')
