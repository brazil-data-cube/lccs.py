..
    This file is part of Python Client Library for the LCCS Web Service.
    Copyright (C) 2019-2020 INPE.

    Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installation
============

``lccs.py`` depends essentially on `Requests <https://requests.readthedocs.io/en/master/>`_. Please, read the instructions below in order to install ``lccs.py``.

Production installation
-----------------------

**Under Development!**

Development Installation - GitHub
---------------------------------


Clone the software repository:

.. code-block:: shell

        $ git clone https://github.com/brazil-data-cube/lccs.py.git

Go to the source code folder:

.. code-block:: shell

        $ cd lccs.py

Install in development mode:

.. code-block:: shell

        $ pip3 install -e .[all]

Run the Tests
+++++++++++++

Run the tests:

.. code-block:: shell

        $ ./run-tests.sh


Build the Documentation
+++++++++++++++++++++++

Generate the documentation:

.. code-block:: shell

        $ python setup.py build_sphinx

The above command will generate the documentation in HTML and it will place it under:

.. code-block:: shell

    docs/sphinx/_build/html/

You can open the above documentation in your favorite browser, as:

.. code-block:: shell

    firefox docs/sphinx/_build/html/index.html