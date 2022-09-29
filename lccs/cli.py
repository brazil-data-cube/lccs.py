#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Command line interface for the LCCS-WS client."""
import click

from .lccs import LCCS


class Config:
    """A simple decorator class for command line options."""

    def __init__(self):
        """Initialize of Config decorator."""
        self.url = None
        self.service = None
        self.access_token = None
        self.language = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--url', default='http://127.0.0.1:5000/',
              help='The LCCS server address (an URL).')
@click.option('--access-token', default=None, help='Personal Access Token of the BDC Auth')
@click.version_option()
@pass_config
def cli(config, url, access_token=None, language=None):
    """LCCS-WS Client on command line."""
    config.url = url
    config.service = LCCS(url=url, access_token=access_token, language=language)


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classification_systems(config: Config, verbose):
    """Return the list of available classification systems in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available classification systems... ',
                    bold=False, fg='black')

        for cs in config.service.classification_systems:
            click.secho(f'\t\t- {cs}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        for cs in config.service.classification_systems:
            click.secho(f'{cs}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classification_system_description(config: Config, system, verbose):
    """Return information for a given classification system."""
    retval = config.service.classification_system(system=system)

    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the classification system metadata... ',
                    bold=False, fg='black')

        for ds_key, ds_value in retval.items():
            click.secho(f'\t\t- {ds_key}: {ds_value}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        for ds_key, ds_value in retval.items():
            click.secho(f'- {ds_key}: {ds_value}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classes(config: Config, system, verbose):
    """Return the list of available classes given a classification system in the service provider."""
    class_system = config.service.classification_system(system=system)

    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the the list of classes for a given classification system.... ',
                    bold=False, fg='black')
        for cv in class_system.classes():
            click.secho(f'\t\t- {cv.name}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')
    else:
        for cv in class_system.classes():
            click.secho(f'{cv.name}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('--system_class', type=click.STRING, required=True, help='The class name or id.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def class_describe(config: Config, system, system_class, verbose):
    """Return information for a classes given a classification system in the service provider."""
    classification_system = config.service.classification_system(system=system)
    retval = classification_system.classes(system_class)

    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the class metadata... ',
                    bold=False, fg='black')

        for ds_key, ds_value in retval.items():
            click.secho(f'\t\t- {ds_key}: {ds_value}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        for ds_key, ds_value in retval.items():
            click.secho(f'{ds_key}: {ds_value}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def available_mappings(config: Config, system, verbose):
    """Return the list of available mappings."""
    retval = config.service.available_mappings(system_source=system)

    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available for a given classification system ... ',
                    bold=False, fg='black')

        for mp in retval:
            click.secho(f'\t\t- {mp}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')
    else:
        for mp in retval:
            click.secho(f'{mp}', bold=True, fg='green')


@cli.command()
@click.option('--system-source', type=click.STRING, required=True,
              help='The classification system source (Identifier by name-version or the ID).')
@click.option('--system-target', type=click.STRING, required=True, default=None,
              help='The classification system target (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def mappings(config: Config, system_source, system_target, verbose):
    """Return the mapping."""
    retval = config.service.mappings(system_source=system_source, system_target=system_target)

    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the mapping ... ',
                    bold=False, fg='black')

        click.secho(f'\t- {retval}', bold=True, fg='green')
        click.secho('\tFinished!', bold=False, fg='black')

    else:
        click.secho(f'\t- {retval}', bold=True, fg='green')


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def style_formats(config: Config, verbose):
    """Return the list of available style formats in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available styles formats... ',
                    bold=False, fg='black')

        for style in config.service.available_style_formats():
            click.secho(f'\t\t- {style.name}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        for style in config.service.available_style_formats():
            click.secho(f'{style.name}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def styles(config: Config, system, verbose):
    """Return the style format available for a specific classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available styles formats... ',
                    bold=False, fg='black')

        for style in config.service.style_formats(system):
            click.secho(f'\t\t- {style.name}', bold=True, fg='green')

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        for style in config.service.style_formats(system):
            click.secho(f'{style.name}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or ID).')
@click.option('--style_format', type=click.STRING, required=True, default=None,
              help='The style format name or id.')
@click.option('-o', '--output', help='Output to a file', type=click.Path(dir_okay=True), required=False)
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def style_file(config: Config, system_name, style_format_name, output, verbose):
    """Return and save the style for a specific classification system and style format in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available styles formats... ',
                    bold=False, fg='black')

    if output:
        config.service.get_style(system_name=system_name, format_name=style_format_name, path=output)
        click.secho(f'Style file save in {output}', bold=True, fg='green')

    else:
        config.service.get_style(system_name=system_name, format_name=style_format_name)
        click.secho(f'Style file save', bold=True, fg='green')


@cli.command()
@click.option('--system_source', type=click.STRING, required=True,
              help='The classification system source (Identifier by name-version or ID).')
@click.option('--system_target', type=click.STRING, required=True, default=None,
              help='The classification system target (Identifier by name-version or ID).')
@click.option('--mappings_path', type=click.Path(exists=True), required=True,  help='Json file with the mapping')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_mapping(config: Config, system_source, system_target, mappings_path, verbose):
    """Add a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new mapping ... ', bold=False, fg='black')

    click.secho(f'Added Mapping between {system_source} and '
                f'{system_target}', bold=True, fg='green')

    config.service.add_mapping(system_source=system_source,
                               system_target=system_target,
                               mappings=mappings_path)

    click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or ID).')
@click.option('--style_format', type=click.STRING, required=True, default=None,
              help='The style format name or id.')
@click.option('--style_path', type=click.Path(exists=True), required=True,  help='The style file path.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_style(config: Config, system, style_format, style_path, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system style ... ', bold=False, fg='black')

    config.service.add_style(system=system, style_path=style_path, style_format=style_format)

    click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--name', type=click.STRING, required=True, default=None,
              help='The style format name.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_style_format(config: Config, name, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system style ... ', bold=False, fg='black')

        config.service.add_style_format(name=name)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.add_style_format(name=name)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='The classification system name.')
@click.option('--authority_name', type=click.STRING, required=True, default=None,
              help='The classification system authority name.')
@click.option('--version', type=click.STRING, required=True, default=None,
              help='The classification system version.')
@click.option('--description', type=(str, str), required=True, default=None,
              help='The classification system description.')
@click.option('--title', type=(str, str), required=True, default=None,
              help='The classification system title')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_classification_system(config: Config, name, authority_name, version, title, description, verbose):
    """Add a new classification system."""
    title_pt, title_en = title
    description_pt, description_en = description

    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system ... ', bold=False, fg='black')

        config.service.add_classification_system(name=name,
                                                 authority_name=authority_name,
                                                 version=version,
                                                 title={'en': title_en, 'pt-br': title_pt},
                                                 description={'en': description_en, 'pt-br': description_pt})

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.add_classification_system(name=name,
                                                 authority_name=authority_name,
                                                 version=version,
                                                 title={'en': title_en, 'pt-br': title_pt},
                                                 description={'en': description_en, 'pt-br': description_pt})


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or ID).')
@click.option('--classes_path', type=click.Path(exists=True), required=True,  help='Json file with classes')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_classes(config: Config, system, classes_path, verbose):
    """Add a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new mapping ... ', bold=False, fg='black')

        config.service.add_classes(system=system, classes=classes_path)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.add_classes(system=system, classes=classes_path)
        click.secho(f'Added classes for {system}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_classification_system(config: Config, system, verbose):
    """Delete a specific classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the classification system ... ',
                    bold=False, fg='black')

        config.service.delete_classification_system(system=system)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.delete_classification_system(system=system)

        click.secho(f'\t - Deleted classification system: {system}!', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('--class_name_or_id', type=click.STRING, required=True, help='The class name or ID.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_class(config: Config, system, class_name_or_id, verbose):
    """Delete class of a classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting class... ',
                    bold=False, fg='black')

        config.service.delete_class(system=system, class_name_or_id=class_name_or_id)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.delete_class(system=system, class_name_or_id=class_name_or_id)
        click.secho(f'\t Deleted class {class_name_or_id} of classification system {system}', bold=True, fg='green')


@cli.command()
@click.option('--style_format', type=click.STRING, required=True, default=None,
              help='The style format name or id.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_style_format(config: Config, style_format, verbose):
    """Delete a style format."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the style format ... ', bold=False, fg='black')

        config.service.delete_style_format(format=style_format)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.delete_style_format(format=style_format)

        click.secho(f'\t Deleted style format {style_format}', bold=True, fg='green')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or ID).')
@click.option('--style_format', type=click.STRING, required=True, default=None,
              help='The style format name or id.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_style(config: Config, system, style_format, verbose):
    """Delete a style for a classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the style ... ', bold=False, fg='black')

        config.service.delete_style(system=system, style_format=style_format)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        config.service.delete_style(system=system, style_format=style_format)


@cli.command()
@click.option('--system_source', type=click.STRING, required=True,
              help='The classification system source (Identifier by name-version or ID).')
@click.option('--system_target', type=click.STRING, required=True, default=None,
              help='The classification system target (Identifier by name-version or ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_mapping(config: Config, system_source, system_target, verbose):
    """Delete a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the mapping ... ', bold=False, fg='black')

        config.service.delete_mapping(system_source=system_source, system_target=system_target)

        click.secho('\tFinished!', bold=False, fg='black')
    else:
        config.service.delete_mapping(system_source=system_source, system_target=system_target)

