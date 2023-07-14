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
    click.echo("Setup")


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
