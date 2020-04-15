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
@click.option('--url', type=click.STRING, default='http://localhost:5000/lccs',
              help='The LCCS server address (an URL).')
@pass_config
def cli(config, url):
    """LCCS on command line."""
    config.url = url

@cli.command()
@pass_config
def classification_systems(config):
    """Return the list of available classification systems in the service provider."""
    service = lccs(config.url)

    retval = service.classification_systems

    pprint(retval)

@cli.command()
@click.option('--system_id', type=click.STRING, required=True, help='The classification system id (name).')
@pass_config
def classification_systems_describe(config, system_id):
    """Return information for a given classification system."""
    service = lccs(config.url)

    retval = service.classification_system(system_id=system_id)

    pprint(retval)

@cli.command()
@click.option('--system_id', type=click.STRING, required=True, help='The classification system id (name).')
@pass_config
def classes(config, system_id):
    """Return the list of available classes given a classification system in the service provider."""
    service = lccs(config.url)

    class_system = service.classification_system(system_id=system_id)


    retval = class_system.classes()

    result = list()

    for i in retval:
        result.append(i['name'])

    pprint(result)

@cli.command()
@click.option('--system_id', type=click.STRING, required=True, help='The classification system id (name).')
@click.option('--class_id', type=click.STRING, required=True, help='The Class id (name).')
@pass_config
def class_describe(config, system_id, class_id):
    """Return information for a classes given a classification system in the service provider."""
    service = lccs(config.url)

    class_system = service.classification_system(system_id=system_id)

    retval = class_system.classes(class_id=class_id)

    pprint(retval)

@cli.command()
@click.option('--system_id_source', type=click.STRING, required=True, help='The classification system source (name).')
@pass_config
def avaliable_mappings(config, system_id_source):
    """Return the list of available mappings."""
    service = lccs(config.url)

    retval = service.avaliable_mappings(system_id_source=system_id_source)

    pprint(retval)

@cli.command()
@click.option('--system_id_source', type=click.STRING, required=True, help='The classification system source (name).')
@click.option('--system_id_target', type=click.STRING, required=True, default=None, help='The classification system source (name)..')
@pass_config
def mappings(config, system_id_source, system_id_target):
    """Return the classes mappings."""
    service = lccs(config.url)

    retval = service.mappings(system_id_source=system_id_source, system_id_target=system_id_target)

    pprint(retval)