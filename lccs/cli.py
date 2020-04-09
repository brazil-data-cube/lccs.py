#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2019 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Command line interface for the LCCS client."""

from pprint import pprint

import click

from .lccs import lccs


class Config:
    """A simple decorator class for command line options."""

    def __init__(self):
        """Inicialize of Config decorator."""
        self.url = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--url', type=click.STRING, default='http://localhost',
              help='The LCCS server address (an URL).')
@pass_config
def cli(config, url):
    """LCCS on command line."""
    config.url = url


@cli.command()
@click.option('--system_id', type=click.STRING, required=False, help='The classification system id (name).')
@pass_config
def classification_systems(config, system_id):
    """Return the list of available classification systems in the service provider."""
    service = lccs(config.url)

    if system_id is not None:
        retval = service.classification_system(system_id=system_id)
    else:
        retval = service.classification_systems()

    pprint(retval)


@cli.command()
@click.argument('system_id_source', type=click.STRING, required=False)
@click.argument('system_id_target', type=click.STRING, required=False)
@pass_config
def mappings(config, system_id_source, system_id_target):
    """Return the list of available mappings."""
    service = lccs(config.url)

    retval = service.mappings(system_id_source=system_id_source, system_id_target=system_id_target)

    pprint(retval)
