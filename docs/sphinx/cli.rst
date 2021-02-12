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

    lccs, version 0.6.0


To list the available classification systems in a service, use the ``classification-systems`` command and provides a URL to the ``--url`` option::

    lccs --url 'http://brazildatacube.dpi.inpe.br/dev/lccs/' classification-systems


The above command will return a list of classification system names as::

    BDC
    IBGE
    PRODES
    MapBiomas5

To get more information about a specific classification system, use the ``classification-systems-describe`` command::

    lccs --url 'http://brazildatacube.dpi.inpe.br/dev/lccs/' classification-systems-describe --system_name 'PRODES-1.0'

Output::

        - authority_name: Projeto de Mapeamento Anual da Cobertura e Uso do Solo no Brasil (MapBiomas)
        - description: O Projeto de Mapeamento Anual da Cobertura e Uso do Solo do Brasil é uma iniciativa que envolve uma rede colaborativa com especialistas nos biomas, usos da terra, sensoriamento remoto, SIG e ciência da computação que utiliza processamento em nuvem e classificadores automatizados desenvolvidos e operados a partir da plataforma Google Earth Engine para gerar uma série histórica de mapas anuais de cobertura e uso da terra do Brasil.
        - id: 32
        - links: [{'href': 'http://brazildatacube.dpi.inpe.br/dev/lccs/classification_system', 'rel': 'parent', 'title': 'Link to this document', 'type': 'application/json'}, ..]
        - name: Mapbiomas5
        - version: 5


List the available classes of a classification system, use the ``classes`` command::

    lccs --url 'http://brazildatacube.dpi.inpe.br/dev/lccs/' classes --system_name 'PRODES-1.0'

The above command will return a list of classes of PRODES as::

    Desmatamento
    Floresta
    Hidrografia
    Não Floresta
    Nuvem
    Resíduo

To get more information about a specific class, use the ``class-describe`` command::

    lccs --url 'http://brazildatacube.dpi.inpe.br/dev/lccs/' class-describe --system_name 'PRODES-1.0' --class_name 'Desflorestamento'

The above command will return a::

    - classification_system_id: 1
    - code: DESFLORESTAMENTO
    - description:
    - id: 1
    - links: [[{'href': 'http://brazildatacube.dpi.inpe.br/dev/lccs/classification_system/1/classes/1', 'rel': 'self', 'title': 'Link to this document', 'type': 'application/json'},...]
    - name: Desflorestamento


Retrieve all available classification system mappings, use the ``available-mappings`` command::

    lccs --url 'http://brazildatacube.dpi.inpe.br/dev/lccs/' available-mappings --system_name_source 'TerraClass_AMZ'

The above command will return a list of classification systems as::

    PRODES


To get a mapping between classification systems, use the ``mappings`` command::

    lccs --url 'http://brazildatacube.dpi.inpe.br/dev/lccs/' mappings --system_id_source 'TerraClass_AMZ' --system_id_target 'PRODES'


Output::

    Classification Source: TerraClass_AMZ
    Classification Target: PRODES
    {'degree_of_similarity': 1.0, 'description': '', 'links': [{'href': 'http://brazildatacube.dpi.inpe.br/dev/lccs/classification_system/TerraClass_AMZ/classes/Agricultura Anual', 'rel': 'item', 'title': 'Link to the source class', 'type': 'application/json'}, {'href': 'http://brazildatacube.dpi.inpe.br/dev/lccs/classification_system/TerraClass_AMZ/classes/Desmatamento', 'rel': 'item', 'title': 'Link to target class', 'type': 'application/json'}], 'source': 'Agricultura Anual', 'source_id': 85, 'target': 'Desmatamento', 'target_id': 175}
    {'degree_of_similarity': 1.0, 'description': '', 'links': [{'href': 'http://brazildatacube.dpi.inpe.br/dev/lccs/classification_system/TerraClass_AMZ/classes/Área Não Observada', 'rel': 'item', 'title': 'Link to the source class', 'type': 'application/json'}, {'href': 'http://brazildatacube.dpi.inpe.br/dev/lccs/classification_system/TerraClass_AMZ/classes/Nuvem', 'rel': 'item', 'title': 'Link to target class', 'type': 'application/json'}], 'source': 'Área Não Observada', 'source_id': 86, 'target': 'Nuvem', 'target_id': 179}

.. note::

    For more information, type in the command line::

        lccs --help
