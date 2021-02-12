#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Command line interface for the LCCS client."""
import click

from .lccs import LCCS


class Config:
    """A simple decorator class for command line options."""

    def __init__(self):
        """Initialize of Config decorator."""
        self.url = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--url', default='http://127.0.0.1:5000/',
              help='The LCCS server address (an URL).')
@click.version_option()
@pass_config
def cli(config, url):
    """LCCS on command line."""
    config.url = url


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classification_systems(config, verbose):
    """Return the list of available classification systems in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available classification systems... ',
                    bold=False, fg='black')

    service = LCCS(config.url)

    if verbose:
        for cs in service.classification_systems:
            click.secho(f'\t\t- {cs}', bold=True, fg='green')
    else:
        for cs in service.classification_systems:
            click.secho(f'{cs}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True, help='The classification system name (name-version).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classification_systems_description(config, system_name, verbose):
    """Return information for a given classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the classification system metadata... ',
                    bold=False, fg='black')

    service = LCCS(config.url)

    retval = service.classification_system(system_name=system_name)

    for ds_key, ds_value in retval.items():
        click.secho(f'\t- {ds_key}: {ds_value}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True, help='The classification system name (name-version).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classes(config, system_name, verbose):
    """Return the list of available classes given a classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the the list of classes for a given classification system.... ',
                    bold=False, fg='black')

    service = LCCS(config.url)

    class_system = service.classification_system(system_name=system_name)

    if verbose:
        for cv in class_system.classes:
            click.secho(f'\t\t- {cv.name}', bold=True, fg='green')
    else:
        for cv in class_system.classes:
            click.secho(f'{cv.name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True, help='The classification system name (name-version).')
@click.option('--class_name', type=click.STRING, required=True, help='The class name.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def class_describe(config, system_name, class_name, verbose):
    """Return information for a classes given a classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the class metadata... ',
                    bold=False, fg='black')

    service = LCCS(config.url)

    class_system = service.classification_system(system_name=system_name)

    retval = class_system.get_class(class_name=class_name)

    for ds_key, ds_value in retval.items():
        click.secho(f'\t- {ds_key}: {ds_value}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True, help='The classification system name (name-version).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def available_mappings(config, system_name, verbose):
    """Return the list of available mappings."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available for a given classification system ... ',
                    bold=False, fg='black')
    service = LCCS(config.url)
    retval = service.available_mappings(system_source_name=system_name)

    if verbose:
        for mp in retval:
            click.secho(f'\t\t- {mp}', bold=True, fg='green')
    else:
        for mp in retval:
            click.secho(f'{mp}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_id_source', type=click.STRING, required=True, help='The classification system source.')
@click.option('--system_id_target', type=click.STRING, required=True, default=None,
              help='The classification system target..')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def mappings(config, system_id_source, system_id_target, verbose):
    """Return the classes mappings."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the mapping ... ',
                    bold=False, fg='black')

    service = LCCS(config.url)
    
    retval = service.mappings(system_id_source=system_id_source, system_id_target=system_id_target)

    if verbose:
        click.secho(f'\t- Classification System Source: {retval["source_classification_system"]}', bold=True, fg='green')
        click.secho(f'\t- Classification System Target: {retval["target_classification_system"]}', bold=True, fg='green')

        for mp in retval['mappings']:
            click.secho(f'\t\t- Class Source: {mp["source"]}', bold=True, fg='green')
            click.secho(f'\t\t- Class Target: {mp["target"]}', bold=True, fg='green')
            click.secho(f'\t\t\tDegree of similarity: {mp["degree_of_similarity"]}', bold=True, fg='green')
            click.secho(f'\t\t\tDescription: {mp["description"]}', bold=True, fg='green')
            click.secho(f'\t\t\tClass Source id: {mp["source_id"]}', bold=True, fg='green')
            click.secho(f'\t\t\tClass Target id: {mp["target_id"]}', bold=True, fg='green')
            click.secho(f'\t\t\tLinks: {mp["links"]}', bold=True, fg='green')

    else:
        click.secho(f'Classification Source: {retval["source_classification_system"]}', bold=True, fg='green')
        click.secho(f'Classification Target: {retval["target_classification_system"]}', bold=True, fg='green')

        for mp in retval['mappings']:
            click.secho(f'{mp}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_id_source', type=click.STRING, required=True, help='The classification system source.')
@click.option('--system_id_target', type=click.STRING, required=True, default=None,
              help='The classification system target.')
@click.option('--mappings_path', type=click.Path(exists=True), required=True,  help='File path with the mapping')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_mapping(config, system_id_source, system_id_target, mappings_path, verbose):
    """Add a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new mapping ... ', bold=False, fg='black')

    service = LCCS(config.url)

    retval = service.add_mapping(system_id_source=system_id_source, system_id_target=system_id_target,
                                 mappings_path=mappings_path)

    click.secho(f'Added Mapping between {retval["source_classification_system"]} and '
                f'{retval["target_classification_system"]}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_id', type=click.STRING, required=True, help='The classification system source.')
@click.option('--style_format', type=click.STRING, required=True, default=None,
              help='The style file format.')
@click.option('--style_path', type=click.Path(exists=True), required=True,  help='The style file path.')
@click.option('--extension', type=click.STRING, required=True, help='The style extension type.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_style(config, system_id, style_format, style_path, extension, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system style ... ', bold=False, fg='black')

    service = LCCS(config.url)

    retval = service.add_style(system_id=system_id, style_format=style_format, style_path=style_path,
                               extension=extension)

    click.secho(f'{retval}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='The classification system name.')
@click.option('--authority_name', type=click.STRING, required=True, default=None,
              help='The classification system authority name.')
@click.option('--description', type=click.STRING, required=True, default=None,
              help='The classification system description.')
@click.option('--version', type=click.STRING, required=True, default=None,
              help='The classification system version.')
@click.option('--file_path', type=click.Path(exists=True), required=True,  help='JSON file with classes of classification system.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_classification_system(config, name, authority_name, description, version, file_path, verbose):
    """Add a new classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system ... ', bold=False, fg='black')

    service = LCCS(config.url)

    cs = service.add_classification_system(name=name, authority_name=authority_name, description=description,
                                           version=version, file_path=file_path)

    click.secho(f' Classification System {cs["name"]} added!', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')
