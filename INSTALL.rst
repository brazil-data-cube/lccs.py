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


Installation
============

Development Installation
------------------------

Pre-Requirements
++++++++++++++++


The ``Python Client Library for LCCS-WS`` (``lccs.py``) depends essentially on:

- `Requests <https://requests.readthedocs.io/en/master/>`_

- `Click <https://pocoo-click.readthedocs.io/en/latest/>`_


 Please, read the instructions below in order to install ``lccs.py``.

Clone the Software Repository
+++++++++++++++++++++++++++++

Use ``git`` to clone the software repository:

.. code-block:: shell

        $ git clone https://github.com/brazil-data-cube/lccs.py.git

Install lccs.py in Development Mode
+++++++++++++++++++++++++++++++++++

Go to the source code folder:

.. code-block:: shell

        $ cd lccs.py

Install in development mode:

.. code-block:: shell

        $ pip3 install -e .[all]

.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.11::

        python3.11 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools


Build the Documentation
+++++++++++++++++++++++

You can generate the documentation based on Sphinx with the following command::

    sphinx-build docs/sphinx docs/sphinx/_build/html


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html


Run the Tests
+++++++++++++

Run the tests:

.. code-block:: shell

        $ ./run-tests.sh


