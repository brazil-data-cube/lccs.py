#
# This file is part of Python Client Library for the LCCS Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Python Client Library for the LCCS Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import pytest

if __name__ == '__main__':
    import tests.tests_lccs
    pytest.main(['--color=auto', '--no-cov', '-v'])