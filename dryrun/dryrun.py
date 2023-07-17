import os
import shutil
import re
import textwrap
import tomllib
from crontab import CronTab
from pathlib import Path

import click


def validate_name(ctx, param, value) -> str:
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


def write_toml(path: Path, name: str, paths: list, time: int, reboot: bool, strict: bool) -> None:
    """
    Writes the config.toml file.
    :return:
    """

    config = f"""
    name = "{name}"
    paths = {list(paths)}
    time = "{time}"
    reboot = {str(reboot).lower()}
    strict = {str(strict).lower()}
    """
    config = textwrap.dedent(config).strip()
    try:
        with open(os.path.join(path, 'config.toml'), 'w') as f:
            f.write(config)
    except FileNotFoundError:
        click.echo(f"Error: Could not locate the file 'config.toml' in directory '{path}'.")
        return
    except PermissionError:
        click.echo(f"Error: No write permissions to the file 'config.toml' in directory '{path}'.")
        return


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
        shutil.copytree(p, os.path.join(new_dir, p.lstrip('/')), dirs_exist_ok=True)
        shutil.copytree(p, os.path.join(old_dir, p.lstrip('/')), dirs_exist_ok=True)
        #shutil.copytree(p, os.path.join(old_dir, os.path.basename(p)), dirs_exist_ok=True)

    # Write parameters to a TOML file
    write_toml(Path(dryrun_dir), name, path, time, reboot, strict)

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
    home_dir = os.path.expanduser("~")
    dryrun_dir = os.path.join(home_dir, '.dryrun', name)
    config_file = os.path.join(dryrun_dir, 'config.toml')

    if not os.path.isfile(config_file):
        click.echo(f"Error: Configuration file does not exist for dryrun '{name}'.")
        return

    # Load config
    with open(config_file, 'rb') as f:
        config = tomllib.load(f)

    time = time or config.get('time')
    reboot = reboot or config.get('reboot')
    strict = strict or config.get('strict')

    new_dir = os.path.join(dryrun_dir, 'new')
    old_dir = os.path.join(dryrun_dir, 'old')

    paths = config.get('paths', [])

    # Copy new files to original locations
    for p in paths:
        dest = p
        shutil.copytree(os.path.join(new_dir, p.lstrip('/')), dest, dirs_exist_ok=True)

    # Create cron job
    cron = CronTab(user='root')
    command = f'python3 {os.path.realpath(__file__)} cli revert --name {name}'
    job = cron.new(command=command)
    job.setall(f'*/{time} * * * *')
    job.set_comment(name)  # Add this line

    # Write cron job
    cron.write()

    click.echo(f"Dryrun '{name}' is now running.")


@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
def stop(name) -> None:
    """
    Stops the dry run.
    :param name:
    :return:
    """
    # Remove cron job
    cron = CronTab(user='root')
    cron.remove_all(comment=name)
    cron.write()

    click.echo(f"Dryrun '{name}' has been stopped.")


@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
def revert(name) -> None:
    """
    Reverts the changes made by the dry run.
    :param name:
    :return:
    """
    home_dir = os.path.expanduser("~")
    dryrun_dir = os.path.join(home_dir, '.dryrun', name)
    config_file = os.path.join(dryrun_dir, 'config.toml')

    if not os.path.isfile(config_file):
        click.echo(f"Error: Configuration file does not exist for dryrun '{name}'.")
        return

    # Load config
    with open(config_file, 'r') as f:
        config = tomllib.load(f)

    old_dir = os.path.join(dryrun_dir, 'old')

    paths = config.get('paths', [])

    # Replace new files with old ones
    for p in paths:
        shutil.rmtree(p)
        shutil.copytree(os.path.join(old_dir, p.lstrip('/')), p)

    click.echo(f"Dryrun '{name}' has been reverted.")


@cli.command()
@click.option('--name', '-n', type=str, callback=validate_name, help='Name of the dryrun.')
def remove(name) -> None:
    """
    Removes the dry run.
    :param name:
    :return:
    """
    # Find the path to the home directory
    home_dir = os.path.expanduser("~")
    dryrun_dir = os.path.join(home_dir, '.dryrun', name)

    # Check if the directory exists
    if not os.path.isdir(dryrun_dir):
        click.echo(f"Error: Dryrun '{name}' does not exist.")
        return

    # Try to remove the directory and handle potential exceptions
    try:
        shutil.rmtree(dryrun_dir)
        click.echo(f"Dryrun '{name}' has been successfully removed.")
    except FileNotFoundError:
        click.echo(f"Error: Dryrun '{name}' does not exist.")
    except PermissionError:
        click.echo(f"Error: You do not have the necessary permissions to remove dryrun '{name}'.")
    except OSError as e:
        click.echo(f"Error: {e}")


if __name__ == '__main__':
    cli()
