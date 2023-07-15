import os
import shutil
import re
from pathlib import Path

import click


def validate_name(ctx, param, value):
    """
    Validates the name of the dry run.
    :param ctx:
    :param param:
    :param value:
    :return:
    """
    if not re.match(r'^[a-zA-Z0-9_-]*$', value):
        raise click.BadParameter('Name should only contain alphanumeric characters, underscores, and hyphens.')
    return value


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
@click.option('--path',
              '-p',
              multiple=True,
              type=str,
              help='Path of the files that will be backed up and replaced for testing.')
@click.option('--time',
              '-t',
              default=5,
              help='How long the files need to be there before replacing them back with the original ones.')
@click.option('--reboot', '-r', is_flag=True, default=False, help='Reboot after a revert.')
@click.option('--strict', '-s', is_flag=True, default=False, help='Run tests on the files.')
def setup(name: str, path, time, reboot, strict) -> None:
    """
    Sets up the dry run.
    :param name:
    :param path:
    :param time:
    :param reboot:
    :param strict:
    :return:
    """
    # Find the path to the home directory
    home_dir = os.path.expanduser("~")
    dryrun_dir = os.path.join(home_dir, '.dryrun', name)

    # Create .dryrun directory if it does not exist
    os.makedirs(dryrun_dir, exist_ok=True)

    # Create 'new' and 'old' directories inside
    old_dir = os.path.join(dryrun_dir, 'old')
    new_dir = os.path.join(dryrun_dir, 'new')
    os.makedirs(old_dir, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)

    # Copy everything from each specified path to the 'old' directory
    for p in path:
        shutil.copytree(p, os.path.join(old_dir, p.lstrip('/')), dirs_exist_ok=True)

    # Write parameters to a TOML file
    config = f"""
    name = "{name}"
    paths = {list(path)}
    time = "{time}"
    reboot = {str(reboot).lower()}
    strict = {str(strict).lower()}
    """
    try:
        with open(os.path.join(dryrun_dir, 'config.toml'), 'w') as f:
            f.write(config)
    except FileNotFoundError:
        click.echo(f"Error: Could not locate the file 'config.toml' in directory '{dryrun_dir}'.")
        return
    except PermissionError:
        click.echo(f"Error: No write permissions to the file 'config.toml' in directory '{dryrun_dir}'.")
        return

    click.echo(f"Setup completed for dryrun '{name}'.")


@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
@click.option('--time',
              '-t',
              default=5,
              help='How long the files need to be there before replacing them back with the original ones.')
@click.option('--reboot', '-r', is_flag=True, default=False, help='Reboot after a revert.')
@click.option('--strict', '-s', is_flag=True, default=False, help='Run tests on the files.')
def run(name, time, reboot, strict) -> None:
    """
    Runs the dry run.
    :param name:
    :param time:
    :param reboot:
    :param strict:
    :return:
    """
    # Insert your run logic here



@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
def stop(name) -> None:
    """
    Stops the dry run.
    :param name:
    :return:
    """
    # Insert your stop logic here
    click.echo("Stop")


@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
def remove(name) -> None:
    """
    Removes the dry run.
    :param name:
    :return:
    """
    # Insert your remove logic here
    click.echo("Remove")


if __name__ == '__main__':
    cli()
