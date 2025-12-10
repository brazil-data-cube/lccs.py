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
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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

console = Console()


@click.group()
@click.option(
    "--url", default="http://127.0.0.1:5000/", help="The LCCS server address (an URL)."
)
@click.option(
    "--access-token", default=None, help="Personal Access Token of the BDC KeyCloak"
)
@click.option("--language", default="pt-br", help="The language of the response.")
@click.version_option()
@pass_config
def cli(config, url, access_token=None, language=None):
    """LCCS-WS Client on command line."""
    config.url = url
    config.service = LCCS(url=url, access_token=access_token, language=language)


@cli.command()
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def classification_systems(config: Config, verbose):
    """Return the list of available classification systems in the service provider."""
    if verbose:
        console.print(f"[bold black]Server:[/bold black] [green]{config.url}[/green]")
        console.print(
            "[black]\tRetrieving the list of available classification systems...[/black]"
        )

        table = Table(
            title="Available Classification Systems",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Title", style="green", no_wrap=True)
        table.add_column("Version", style="green", no_wrap=True)
        table.add_column("Identifier", style="green", no_wrap=True)

        for cs in config.service.classification_systems:
            table.add_row(cs["title"], cs["version"], cs["identifier"])

        console.print(table)

        console.print("[black]\tFinished![/black]")

    else:
        for cs in config.service.classification_systems:
            console.print(f"[green]{cs}[/green]", style="bold")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or the ID).",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def classification_system_description(config: Config, system, verbose):
    """Return information for a given classification system."""
    retval = config.service.classification_system(system=system)

    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tRetrieving the classification system metadata... ",
            bold=False,
            fg="black",
        )

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="bold magenta", no_wrap=True)
        table.add_column("Value", style="green")

        for key, value in retval.items():
            if isinstance(value, list):
                value = "\n".join(f"- {item}" for item in value)
            elif isinstance(value, dict):
                value = "\n".join(f"{k}: {v}" for k, v in value.items())
            table.add_row(str(key), str(value))

        panel = Panel(
            table, title="[bold green]Metadata[/bold green]", border_style="bright_blue"
        )
        console.print(panel)

    else:
        for ds_key, ds_value in retval.items():
            click.secho(f"- {ds_key}: {ds_value}", bold=True, fg="green")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or the ID).",
)
@click.option(
    "--style_format", type=click.STRING, required=False, help="The style format."
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def classes(config: Config, system, style_format, verbose):
    """Return the list of available classes given a classification system in the service provider."""
    class_system = config.service.classification_system(system=system)

    if verbose:
        console.print(f"[bold green]Server:[/bold green] [green]{config.url}[/green]")
        console.print(
            "[green]\tRetrieving the list of classes for a given classification systems...[/green]"
        )

        table = Table(title="Classes", show_header=True, header_style="bold magenta")
        table.add_column("Title", style="cyan")
        table.add_column("Color", style="green", no_wrap=True)
        table.add_column("Description", style="green", no_wrap=False, max_width=50)
        table.add_column("Code", style="green", no_wrap=True)
        table.add_column("Name", justify="right", style="cyan")
        table.add_column("Class Parent", justify="right", style="cyan")

        for cv in class_system.classes(style_format_name_or_id=style_format):
            table.add_row(
                cv.title,
                cv.color,
                cv.description,
                cv.code,
                cv.name,
                cv.class_parent_name,
            )

        panel = Panel(
            table,
            title=f"[bold green]{class_system.title}[/bold green]",
            expand=False,
            border_style="bright_blue",
        )
        console.print(panel)

        console.print("[black]\tFinished![/black]")

    else:
        for cv in class_system.classes():
            click.secho(f"{cv.name}", bold=True, fg="green")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or the ID).",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def available_mappings(config: Config, system, verbose):
    """Return the list of available mappings."""
    retval = config.service.available_mappings(system_source=system)

    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tRetrieving the list of available for a given classification system ... ",
            bold=False,
            fg="black",
        )

        for mp in retval:
            click.secho(f"\t\t- {mp}", bold=True, fg="green")

        click.secho("\tFinished!", bold=False, fg="black")
    else:
        for mp in retval:
            click.secho(f"{mp}", bold=True, fg="green")


@cli.command()
@click.option(
    "--system-source",
    type=click.STRING,
    required=True,
    help="The classification system source (Identifier by name-version or the ID).",
)
@click.option(
    "--system-target",
    type=click.STRING,
    required=True,
    default=None,
    help="The classification system target (Identifier by name-version or the ID).",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def mappings(config: Config, system_source, system_target, verbose):
    """Return the mapping."""
    retval = config.service.mappings(
        system_source=system_source, system_target=system_target
    )

    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tRetrieving the mapping ... ", bold=False, fg="black")

        click.secho(f"\t- {retval}", bold=True, fg="green")
        click.secho("\tFinished!", bold=False, fg="black")

    else:
        click.secho(f"\t- {retval}", bold=True, fg="green")


@cli.command()
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def style_formats(config: Config, verbose):
    """Return the list of available style formats in the service provider."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tRetrieving the list of available styles formats... ",
            bold=False,
            fg="black",
        )

        for style in config.service.available_style_formats():
            click.secho(f"\t\t- {style.name}", bold=True, fg="green")

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        for style in config.service.available_style_formats():
            click.secho(f"{style.name}", bold=True, fg="green")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or ID).",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def styles(config: Config, system, verbose):
    """Return the style format available for a specific classification system in the service provider."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tRetrieving the list of available styles formats... ",
            bold=False,
            fg="black",
        )

        for style in config.service.style_formats(system):
            click.secho(f"\t\t- {style.name}", bold=True, fg="green")

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        for style in config.service.style_formats(system):
            click.secho(f"{style.name}", bold=True, fg="green")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or ID).",
)
@click.option(
    "--style_format",
    type=click.STRING,
    required=True,
    default=None,
    help="The style format name or id.",
)
@click.option(
    "-o",
    "--output",
    help="Output to a file",
    type=click.Path(dir_okay=True),
    required=False,
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def style_file(config: Config, system, style_format, output, verbose):
    """Return and save the style for a specific classification system and style format in the service provider."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tRetrieving the list of available styles formats... ",
            bold=False,
            fg="black",
        )

    if output:
        config.service.get_style(system=system, style_format=style_format, path=output)
        click.secho(f"Style file save in {output}", bold=True, fg="green")

    else:
        config.service.get_style(system=system, style_format=style_format)
        click.secho(f"Style file save", bold=True, fg="green")


@cli.command()
@click.option(
    "--system_source",
    type=click.STRING,
    required=True,
    help="The classification system source (Identifier by name-version or ID).",
)
@click.option(
    "--system_target",
    type=click.STRING,
    required=True,
    default=None,
    help="The classification system target (Identifier by name-version or ID).",
)
@click.option(
    "--mappings_path",
    type=click.Path(exists=True),
    required=True,
    help="Json file with the mapping",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def add_mapping(config: Config, system_source, system_target, mappings_path, verbose):
    """Add a mapping between classification systems."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tAdding new mapping ... ", bold=False, fg="black")

    click.secho(
        f"Added Mapping between {system_source} and " f"{system_target}",
        bold=True,
        fg="green",
    )

    config.service.add_mapping(
        system_source=system_source, system_target=system_target, mappings=mappings_path
    )

    click.secho("\tFinished!", bold=False, fg="black")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or ID).",
)
@click.option(
    "--style_format",
    type=click.STRING,
    required=True,
    default=None,
    help="The style format name or id.",
)
@click.option(
    "--style_path",
    type=click.Path(exists=True),
    required=True,
    help="The style file path.",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def add_style(config: Config, system, style_format, style_path, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tAdding new classification system style ... ", bold=False, fg="black"
        )

    config.service.add_style(
        system=system, style_path=style_path, style_format=style_format
    )

    click.secho("\tFinished!", bold=False, fg="black")


@cli.command()
@click.option(
    "--name",
    type=click.STRING,
    required=True,
    default=None,
    help="The style format name.",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def add_style_format(config: Config, name, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho(
            "\tAdding new classification system style ... ", bold=False, fg="black"
        )

        config.service.add_style_format(name=name)

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        config.service.add_style_format(name=name)


@cli.command()
@click.option(
    "--system_path",
    type=click.Path(exists=True),
    required=True,
    help="Json file with classes",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def add_classification_system(config: Config, system_path, verbose):
    """Add a new classification systems."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tAdding new classification system ... ", bold=False, fg="black")

        config.service.add_classification_system(system_path=system_path)

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        click.secho(f"New classification system created", bold=True, fg="green")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or ID).",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def delete_classification_system(config: Config, system, verbose):
    """Delete a specific classification system."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tDeleting the classification system ... ", bold=False, fg="black")

        config.service.delete_classification_system(system=system)

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        config.service.delete_classification_system(system=system)

        click.secho(
            f"\t - Deleted classification system: {system}!", bold=True, fg="green"
        )


@cli.command()
@click.option(
    "--system", type=click.STRING, required=True, help="The classification system."
)
@click.option(
    "--classes_path",
    type=click.Path(exists=True),
    required=True,
    help="Json file with classes",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def add_classes(config: Config, system, classes_path, verbose):
    """Add a new class into classification systems."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tAdding new mapping ... ", bold=False, fg="black")

    config.service.add_classes(system=system, classes=classes_path)

    click.secho(f"Added classes for {system}", bold=True, fg="green")

    if verbose:
        click.secho("\tFinished!", bold=False, fg="black")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version).",
)
@click.option(
    "--class_name_or_id", type=click.STRING, required=True, help="The class name or ID."
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def delete_class(config: Config, system, class_name_or_id, verbose):
    """Delete class of a classification system in the service provider."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tDeleting class... ", bold=False, fg="black")

        config.service.delete_class(system=system, class_name_or_id=class_name_or_id)

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        config.service.delete_class(system=system, class_name_or_id=class_name_or_id)
        click.secho(
            f"\t Deleted class {class_name_or_id} of classification system {system}",
            bold=True,
            fg="green",
        )


@cli.command()
@click.option(
    "--style_format",
    type=click.STRING,
    required=True,
    default=None,
    help="The style format name or id.",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def delete_style_format(config: Config, style_format, verbose):
    """Delete a style format."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tDeleting the style format ... ", bold=False, fg="black")

        config.service.delete_style_format(format=style_format)

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        config.service.delete_style_format(format=style_format)

        click.secho(f"\t Deleted style format {style_format}", bold=True, fg="green")


@cli.command()
@click.option(
    "--system",
    type=click.STRING,
    required=True,
    help="The classification system (Identifier by name-version or ID).",
)
@click.option(
    "--style_format",
    type=click.STRING,
    required=True,
    default=None,
    help="The style format name or id.",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def delete_style(config: Config, system, style_format, verbose):
    """Delete a style for a classification system."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tDeleting the style ... ", bold=False, fg="black")

        config.service.delete_style(system=system, style_format=style_format)

        click.secho("\tFinished!", bold=False, fg="black")

    else:
        config.service.delete_style(system=system, style_format=style_format)


@cli.command()
@click.option(
    "--system_source",
    type=click.STRING,
    required=True,
    help="The classification system source (Identifier by name-version or ID).",
)
@click.option(
    "--system_target",
    type=click.STRING,
    required=True,
    default=None,
    help="The classification system target (Identifier by name-version or ID).",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@pass_config
def delete_mapping(config: Config, system_source, system_target, verbose):
    """Delete a mapping between classification systems."""
    if verbose:
        click.secho(f"Server: {config.url}", bold=True, fg="black")
        click.secho("\tDeleting the mapping ... ", bold=False, fg="black")

        config.service.delete_mapping(
            system_source=system_source, system_target=system_target
        )

        click.secho("\tFinished!", bold=False, fg="black")
    else:
        config.service.delete_mapping(
            system_source=system_source, system_target=system_target
        )
