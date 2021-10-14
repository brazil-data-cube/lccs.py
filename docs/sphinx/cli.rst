..
    This file is part of Python Client Library for the LCCS Web Service.
    Copyright (C) 2020 INPE.

    Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Running LCCS Client in the Command Line
=======================================

If you want to know the LCCS version, use the option ``--version`` as in::

    lccs --version


Output::

    lccs, version 0.8.0


To list the available classification systems in a service, use the ``classification-systems`` command and provides a URL to the ``--url`` option::

    lccs --url 'https://brazildatacube.dpi.inpe.br/dev/lccs/' --access-token 'change-me' classification-systems


The above command will return a list of classification system names as::

    prodes-1.0
    terraclass-amz-1.0
    deter-amz-1.0

To get more information about a specific classification system, use the ``classification-systems-describe`` command::

    lccs --url 'https://brazildatacube.dpi.inpe.br/dev/lccs/' --access-token 'change-me' classification-system-description --system 'prodes-1.0'

Output::

        - authority_name: INPE
        - description: Annual Deforestation Classification System
        - id: 1
        - identifier: prodes-1.0
        - links: [{'href': 'https://brazildatacube.dpi.inpe.br/dev/lccs/classification_system', 'rel': 'parent', 'title': 'Link to this document', 'type': 'application/json'}, ..]
        - name: prodes
        - title: PRODES
        - version: 1.0
        - version_predecessor: None
        - version_successor: None



List the available classes of a classification system, use the ``classes`` command::

    lccs --url 'https://brazildatacube.dpi.inpe.br/dev/lccs/' --access-token 'change-me' classes --system 'prodes-1.0'

The above command will return a list of classes of PRODES as::

    desflorestamento
    floresta
    hidrografia
    nao-floresta
    nuvem
    residuo


To get more information about a specific class, use the ``class-describe`` command::

    lccs --url 'https://brazildatacube.dpi.inpe.br/dev/lccs/' --access-token 'change-me' class-describe --system 'prodes-1.0' --system_class 'desflorestamento'

The above command will return a::

    - classification_system_id: 1
    - code: DESFLORESTAMENTO
    - description:
    - id: 1
    - links: [[{'href': 'https://brazildatacube.dpi.inpe.br/dev/lccs/classification_system/1/classes/1', 'rel': 'self', 'title': 'Link to this document', 'type': 'application/json'},...]
    - name: desflorestamento
    - title: Deforestation


Retrieve all available classification system mappings, use the ``available-mappings`` command::

    lccs --url 'https://brazildatacube.dpi.inpe.br/dev/lccs/' --access-token 'change-me' available-mappings --system 'terraclass-amz-1.0'

The above command will return a list of classification systems as::

    Classification System [1:prodes - Version 2]


To get a mapping between classification systems, use the ``mappings`` command::

    lccs --url 'https://brazildatacube.dpi.inpe.br/dev/lccs/' mappings --system_id_source 'terraclass-amz-1.0' --system_id_target 'prodes-1.0'


Output::

    Agricultura Anual -> Desmatamento - Degree_of_similarity 0.0
    Área Não Observada -> Nuvem - Degree_of_similarity 0.0

.. note::

    For more information, type in the command line::

        lccs --help

