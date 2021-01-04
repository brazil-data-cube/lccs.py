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

# Return the list of available clasification system for mapping
available_mappings = service.avaliable_mappings(system_id_source='TerraClass_AMZ')

print(available_mappings)
