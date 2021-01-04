..
    This file is part of Python Client Library for the LCCS Web Service.
    Copyright (C) 2019-2020 INPE.

    Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


======================================================================
Python Client Library for Land Cover Classification System Web Service
======================================================================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com//brazil-data-cube/lccs.py/blob/master/LICENSE
        :alt: Software License

.. image:: https://travis-ci.org/brazil-data-cube/lccs.py.svg?branch=master
        :target: https://travis-ci.org/brazil-data-cube/lccs.py
        :alt: Build Status

.. image:: https://coveralls.io/repos/github/brazil-data-cube/lccs.py/badge.svg?branch=master
        :target: https://coveralls.io/github/brazil-data-cube/lccs.py?branch=master
        :alt: Code Coverage Test

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


Using LCCS in the Command Line
==============================

See `CLI.rst <./CLI.rst>`_.

Developer Documentation
=======================

See https://lccspy.readthedocs.io/en/latest.


License
=======

.. admonition::
    Copyright (C) 2019-2020 INPE.

    Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
