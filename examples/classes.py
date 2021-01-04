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
service = LCCS("http://0.0.0.0:5000/")

# Get a specific classification system
# Make sure the classification system is available in service
classification_system = service.classification_system(system_id='TerraClass_AMZ')

# Returns all classes belonging to a specific classification system.
classes = classification_system.classes()
print(classes)
