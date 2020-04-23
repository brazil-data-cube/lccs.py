#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""LCCS Python Client Samples."""

import os

from lccs import lccs

url = os.environ.get('LCCS_SERVER_URL', 'http://0.0.0.0:5000/lccs/')

service = lccs(url)

print("Classificatom System Avaliable on Service:")
print(service.classification_systems)

print("\nInformations about TerraClass_AMZ Classification System:")
class_system = service.classification_system(system_id='TerraClass_AMZ')
print(class_system.description)

print("\nTerraClass_AMZ Classes: \n")
classes = class_system.classes()
print(classes)

print("\nTerraClass_AMZ Desflorestamento informations: \n")
class_desflorestamento = class_system.classes(class_id='Desflorestamento')
print(class_desflorestamento)

all_mapping = service.avaliable_mappings(system_id_source='TerraClass_AMZ')

if all_mapping:

    for target in all_mapping:
        mapping = service.mappings(system_id_source='TerraClass_AMZ', system_id_target=target)

        print("Mapping TerraClass to {}: \n".format(target))
        for mp in mapping:
            print("Source Class: {} | Target Class: {}".format(mp.source_class.name, mp.target_class.name))

styles = service.styles(system_id='TerraClass_AMZ')