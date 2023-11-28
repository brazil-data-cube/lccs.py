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

======================================================================
Python Client Library for Land Cover Classification System Web Service
======================================================================

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
        :target: https://github.com/brazil-data-cube/bdc-catalog/blob/master/LICENSE
        :alt: Software License

.. image:: https://readthedocs.org/projects/lccs/badge/?version=latest
        :target: https://lccs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/lifecycle-maturing-blue.svg
        :target: https://www.tidyverse.org/lifecycle/#maturing
        :alt: Software Life Cycle

.. image:: https://img.shields.io/github/tag/brazil-data-cube/lccs.py.svg
        :target: https://github.com/brazil-data-cube/lccs.py/releases
        :alt: Release

.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord

About
=====

Currently, there are several data sets on regional, national and global scales with information on land use and land cover that aim to support a large number of applications, including the management of natural resources, climate change and its impacts, and biodiversity conservation. These data products are generated using different approaches and methodologies, which present information about different classes of the earth's surface, such as forests, agricultural plantations, among others. Initiatives that generate land use and land cover maps normally develop their own classification system, with different nomenclatures and meanings of the classes used.


In this context, the **LCCS-WS** (**L**\ and **C**\ over **C**\ lassification **S**\ystem **W**\eb **S**\ ervice) aims to provide a simple interface to access the various classification systems in use and their respective classes. Therefore, this service proposes a representation for the classification systems and provides an API to access the classes and their symbolizations. It is also possible to stablish mappings between classes of different systems.

If you want to know more about LCCS service, please, take a look at its `specification <https://github.com/brazil-data-cube/lccs-ws-spec>`_.

Installation
============

See `INSTALL.rst <./INSTALL.rst>`_.


Developer Documentation
=======================

See https://lccs.readthedocs.io/en/latest/.


License
=======

.. admonition::
    Copyright (C) 2023 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
