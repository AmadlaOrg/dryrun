import os
import shutil
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', '-n', type=str, help='Name of the dryrun.')
@click.option('--path', '-p', type=str, help='Path of the files that will be backed up and replaced for testing.')
@click.option('--time',
              '-t',
              default='5min',
              help='How long the files need to be there before replacing them back with the original ones.')
@click.option('--reboot', '-r', is_flag=True, default=False, help='Reboot after a revert.')
@click.option('--strict', '-s', is_flag=True, default=True, help='Run tests on the files.')
def setup(name, path, time, reboot, strict):
    # Insert your setup logic here
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

    # Copy everything from the specified path to the 'old' directory
    shutil.copytree(path, os.path.join(old_dir, path.lstrip('/')), dirs_exist_ok=True)

    click.echo(f"Setup completed for dryrun '{name}'.")


@cli.command()
@click.option('--name', '-n', type=str, help='Name of the dryrun.')
def run(name):
    # Insert your run logic here
    click.echo("Run")


@cli.command()
@click.option('--name', '-n', type=str, help='Name of the dryrun.')
def stop(name):
    # Insert your stop logic here
    click.echo("Stop")


@cli.command()
@click.option('--name', '-n', type=str, help='Name of the dryrun.')
def remove(name):
    # Insert your remove logic here
    click.echo("Remove")


if __name__ == '__main__':
    cli()
