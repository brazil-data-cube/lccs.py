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
service = LCCS("https://brazildatacube.dpi.inpe.br/lccs/")

# Returns the mapping between two classification systems.
# Make sure the classification system is available in service
mapping = service.mappings(system_name_source='PRODES-1.0', system_name_target='TerraClass_AMZ-1.0')

print(mapping)