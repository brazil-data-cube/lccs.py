#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""LCCS Python Client Samples."""

import os
import lccs

print(lccs.__version__)

url = os.environ.get('LCCS_SERVER_URL', 'http://0.0.0.0:5000/')

service = lccs.LCCS(url)

print("Classificatom System Avaliable on Service:")
print(service.classification_systems)

# The examples presented in this code vary depending on the database used. Check the parameters informed.

print("\nInformations about TerraClass_AMZ Classification System:")
class_system = service.classification_system(system_id='TerraClass_AMZ')
print(class_system.description)

print("\nTerraClass_AMZ Classes: \n")
classes = class_system.classes()
print(classes)

print("\nTerraClass_AMZ Desflorestamento informations: \n")
class_desflorestamento = class_system.classes(class_id='Desflorestamento')
print(class_desflorestamento)

all_mapping = service.available_mappings(system_id_source='TerraClass_AMZ')

mapping = service.mappings(system_id_source='TerraClass_AMZ', system_id_target='PRODES')

print("\nMapping {} to {}: \n".format(mapping.source_classification_system, mapping.target_classification_system))

for mp in mapping.mapping:
    print("Source Class: {} | Target Class: {}".format(mp.source_class, mp.target_class))

# Get all styles avaliable for MapBiomas4
styles = service.styles(system_id='MapBiomas4')

print(styles)

# Save Style File
service.get_styles(system_id='MapBiomas4', format_id='QGIS')

# Save Style File passing the path directory
service.get_styles(system_id='MapBiomas4', format_id='QGIS', path='/home/fabiana/Downloads/')