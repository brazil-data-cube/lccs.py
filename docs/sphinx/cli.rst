..
    This file is part of Python Client Library for LCCS-WS.
    Copyright (C) 2023 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.

Usage
=====

If you want to know the LCCS version, use the option ``--version`` as in::

    lccs --version


Output::

    lccs, version 1.0.1


To list the available classification systems in a service, use the ``classification-systems`` command and provides a URL to the ``--url`` option::

    lccs --url 'https://data.inpe.br/bdc/lccs/v1/' --access-token 'change-me' classification-systems


The above command will return a list of classification system names as::

    {'identifier': 'prodes-1.0', 'title': 'PRODES', 'version': '1.0'}
    {'identifier': 'prodes_cerrado-1.0', 'title': 'PRODES_Cerrado', 'version': '1.0'}
    {'identifier': 'deter-cerrado-1.0', 'title': 'DETER Cerrado', 'version': '1.0'}


To get more information about a specific classification system, use the ``classification-systems-describe`` command::

    lccs --url 'https://data.inpe.br/bdc/lccs/v1/' --access-token 'change-me' classification-system-description --system 'prodes-1.0'

Output::

        - authority_name: INPE
        - description: Sistema de Classificação Anual de Desmatamento
        - id: 4
        - identifier: prodes-1.0
        - links: [{'href': 'https://data.inpe.br/bdc/lccs/v1/classification_systems?language=pt-br', 'rel': 'parent', 'title': 'Link to this document', 'type': 'application/json'}, {'href': 'https://data.inpe.br/bdc/lccs/v1/classification_systems/4?language=pt-br', 'rel': 'self', 'title': 'The classification_system', 'type': 'application/json'}, {'href': 'https://data.inpe.br/bdc/lccs/v1/classification_systems/4/classes?language=pt-br', 'rel': 'classes', 'title': 'The classes related to this item', 'type': 'application/json'}, {'href': 'https://data.inpe.br/bdc/lccs/v1/classification_systems/4/style_formats', 'rel': 'styles_formats', 'title': 'The styles formats related to this item', 'type': 'application/json'}, {'href': 'https://data.inpe.br/bdc/lccs/v1/mappings/4', 'rel': 'mappings', 'title': 'The classification system mappings', 'type': 'application/json'}, {'href': 'https://data.inpe.br/bdc/lccs/v1?language=pt-br', 'rel': 'root', 'title': 'API landing page.', 'type': 'application/json'}]
        - name: prodes
        - title: PRODES
        - version: 1.0
        - version_predecessor: None
        - version_successor: None

List the available classes of a classification system, use the ``classes`` command::

    lccs --url 'https://data.inpe.br/bdc/lccs/v1/' --access-token 'change-me' classes --system 'prodes-1.0'

The above command will return a list of classes of PRODES as::

    desflorestamento
    floresta
    hidrografia
    nao-floresta
    nuvem
    residuo


To get more information about a specific class, use the ``class-describe`` command::

    lccs --url 'https://data.inpe.br/bdc/lccs/v1/' --access-token 'change-me' class-describe --system 'prodes-1.0' --system_class 'desmatamento'

The above command will return a::

    - classification_system_id: 1
    - code: DESFLORESTAMENTO
    - description:
    - id: 175
    - links: [[{'href': 'https://brazildatacube.dpi.inpe.br/lccs/classification_system/1/classes/175', 'rel': 'self', 'title': 'Link to this document', 'type': 'application/json'},...]
    - name: desmatamento
    - title: Desmatamento

Retrieve all available classification system mappings, use the ``available-mappings`` command::

    lccs --url 'https://brazildatacube.dpi.inpe.br/lccs/' --access-token 'change-me' available-mappings --system 'terraclass-amz-1.0'

The above command will return a list of classification systems as::

    <Classification System [4:prodes-1.0 - Title: PRODES]>


To get a mapping between classification systems, use the ``mappings`` command::

    lccs --url 'https://data.inpe.br/bdc/lccs/v1/' mappings --system_id_source 'terraclass-amz-1.0' --system_id_target 'prodes-1.0'


Output::

    Agricultura Anual -> Desmatamento - Degree_of_similarity 0.0
    Área Não Observada -> Nuvem - Degree_of_similarity 0.0

.. note::

    For more information, type in the command line::

        lccs --help

