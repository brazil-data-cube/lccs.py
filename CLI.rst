..
    This file is part of Python Client Library for the LCCS Web Service.
    Copyright (C) 2019-2020 INPE.

    Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Running LCCS Client in the Command Line
=======================================

List the available classification systems:

.. code-block:: shell

        lccs --url 'http://localhost:5000/lccs' classification-systems

The above command will return a list of classification system names as:

.. code-block:: shell

    dict_keys(['Deter-A', 'DETER-B', 'PRODES', 'TerraClass_AMZ', 'MapBiomas3.1'])


Retrieve the information given a classification system name (system_id):

.. code-block:: shell

        lccs --url 'http://localhost:5000/lccs' classification-systems-describe --system_id 'PRODES'

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

List the available classes of a classification system given a classification system name (system_id):

.. code-block:: shell

    lccs --url 'http://localhost:5000/lccs' classes --system_id 'PRODES'

The above command will return a list of classes of PRODES as:

.. code-block:: shell

    ['Desflorestamento',
     'Floresta',
     'Hidrografia',
     'Não Floresta',
     'Nuvem',
     'Resíduo']

Retrieve the information of a class given a classification system name (system_id) and class name (class_id):

.. code-block:: shell

    lccs --url 'http://localhost:5000/lccs' class-describe --system_id 'PRODES' --class_id 'Desflorestamento'


The above command will return a JSON document as:

.. code-block:: shell

    {'code': 'DESFLORESTAMENTO',
     'description': '',
     'id': 380,
     'links': [{'href': 'http://localhost:5000/lccs/classification_systems/PRODES/classes/Desflorestamento',
                'rel': 'self'},
               {'href': 'http://localhost:5000/lccs/classification_systems/PRODES/classes',
                'rel': 'parent'},
               {'href': 'http://localhost:5000/lccs/classification_systems/PRODES',
                'rel': 'PRODES'},
               {'href': 'http://localhost:5000/lccs/classification_systems',
                'rel': 'classification_systems'},
               {'href': 'http://localhost:5000/lccs/', 'rel': 'root'}],
     'name': 'Desflorestamento',
     'parent': {}}

Retrieve all avaliable classification system for mappings of a given a classification system name (system_id_source)

.. code-block:: shell

    lccs --url 'http://localhost:5000/lccs' avaliable-mappings --system_id_source 'TerraClass_AMZ'

The above command will return a list of classification systems as:

.. code-block:: shell

    ['PRODES']

.. code-block:: shell

    lccs --url 'http://localhost:5000/lccs' mappings --system_id_source 'TerraClass_AMZ' --system_id_target 'PRODES'

The above command will return a list with classification systems mappings:

.. code-block:: shell

    [{'degree_of_similarity': None,
      'description': None,
      'links': [{'href': 'http://localhost:5000/lccs/classification_systems/TerraClass_AMZ/classes/Agricultura '
                         'Anual',
                 'rel': 'source_class',
                 'title': 'Agricultura Anual'},
                {'href': 'http://localhost:5000/lccs/classification_systems/PRODES/classes/Desflorestamento',
                 'rel': 'target_class',
                 'title': 'Desflorestamento'},
                {'href': 'http://localhost:5000/lccs/', 'rel': 'root'}]}]