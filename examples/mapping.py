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

# Returns the mapping between two classification systems.
# Make sure the classification system is available in service
mappings = service.mappings(system_id_source='TerraClass_AMZ', system_id_target='PRODES')

for mp in mappings.mapping:
    print("Source Class: {} ID: {} | Target Class: {} ID: {}".format(mp.source_class, mp.source_class_id,
                                                                     mp.target_class, mp.target_class_id))

