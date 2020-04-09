..
    This file is part of Python Client Library for the LCCS Web Service.
    Copyright (C) 2019 INPE.

    Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Running LCCS Client in the Command Line
=======================================

List the available classification systems:

.. code-block:: shell

        lccs --url 'http://localhost/lccs_ws' classification-systems

Retrieve the information given a classification system identifier (name):

.. code-block:: shell

        lccs --url 'http://localhost/lccs_ws' classification-systems --system_id 'PRODES'

The above command will return a JSON document as:

.. code-block:: shell

        {'authority_name': 'INPE',
         'description': 'Sistema de Classificação Anual de Desmatamento',
         'id': 3,
         'links': [{'href': 'http://localhost/lccs_ws/classification_systems/PRODES',
                    'rel': 'self'},
                   {'href': 'http://localhost/lccs_ws/classification_systems/PRODES/classes',
                    'rel': 'classes'},
                   {'href': 'http://localhost/lccs_ws/classification_systems',
                    'rel': 'parent'},
                   {'href': 'http://localhost:/lccs_ws/', 'rel': 'root'}],
         'name': 'PRODES',
         'style': [],
         'version': '1.0'}