#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2020 INPE.
#
# Python Client Library for the LCCS-WS is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""LCCS Python Client examples."""

from lccs import LCCS

# Change to the LCCS-WS URL you want to use.
service = LCCS("https://brazildatacube.dpi.inpe.br/lccs/", access_token='change-me', language='en')

# Return the metadata of a specific classification system
# Make sure the classification system is available in service
classification_system = service.classification_system('prodes-1.0')

# You can access specific attributes
print(classification_system.id)
print(classification_system.name)
print(classification_system.title)
print(classification_system.description)
print(classification_system.authority_name)
print(classification_system.version)

