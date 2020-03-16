#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""LCCS Python Client Samples."""

import os
from pprint import pprint

from lccs import lccs

url = os.environ.get('LCCS_SERVER_URL', 'http://0.0.0.0:5000/lccs_ws/')

service = lccs(url)

retval = service.classification_systems()

print("Sistemas de Classificação Disponíveis: \n")
print(retval)

class_system = service.classification_system(system_id='TerraClass')

print("\n Descrição do sistema TerraClass: ")
print(class_system.description)

print("Classes do TerraClass:")
classes = class_system.classes()
pprint(classes)

classes = class_system.classes(class_id='Desflorestamento')
pprint(classes.name)

mapping = service.mappings(system_id_source='TerraClass', system_id_target='PRODES')

print("Mapping TerraClass to PRODES: \n")
for mp in mapping:
    print("Source Class: {} | Target Class: {}".format(mp.source_class.name, mp.target_class.name))
