#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""LCCS Python Client examples."""

import os
import lccs

print(lccs.__version__)

url = os.environ.get('LCCS_SERVER_URL', 'https://brazildatacube.dpi.inpe.br/dev/lccs/')

service = lccs.LCCS('http://127.0.0.1:5000/')

print("Return all classificaton systems available in service")
print(service.classification_systems)

# The examples presented in this code vary depending on the database used. Check the parameters informed.

# Return a specific classification system
class_system = service.classification_system('PRODES-1.0')
print(class_system.description)
print(class_system.name)

# Return a classes of a classification system
classes = class_system.classes
for i in classes:
    print(i.name)

# Return a specific class of a classification system
prodes_desflorestamento = class_system.get_class('Desflorestamento')
print(prodes_desflorestamento.name)

# Get all available mappings for a specific classification system
all_mapping = service.available_mappings(system_source_name='PRODES-1.0')
print(all_mapping)

# Get mapping
mapping = service.mappings(system_name_source='PRODES-1.0', system_name_target='TerraClass_AMZ-1.0')

print(f"\nMapping PRODES-1.0 to TerraClass_AMZ-1.0: \n")

for mp in mapping:
    print(mp)

# Get all styles available for a specific classification system
style_formats = service.style_formats(system_source_name='PRODES-1.0')
for style_f in style_formats:
    print(style_f.name)

# Save a style file of a specific classification system and style format
service.get_style(system_name='PRODES-1.0', format_name='QGIS')

# Save Style File passing the path directory
service.get_style(system_name='PRODES-1.0', format_name='QGIS', path='/home/user/Downloads/')
