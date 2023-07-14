# dryrun

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](./README.md)
[![Language: Français](https://img.shields.io/badge/Langue-Fran%C3%A7ais-blue.svg)](./README.fr.md)

[![Python 3.11](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](#)

Dryrun is a Python-based command-line tool designed to automate the process of testing changes to configuration files. It allows you to backup existing configurations, apply new configurations, and revert to the old configurations automatically after a specified duration or upon command.

This tool is particularly useful for scenarios where you need to test changes that may cause a loss of connectivity or have other significant effects, as it allows you to revert to a previous state automatically.

## Features

* Backup existing configurations
* Apply new configurations
* Automatically revert to old configuration after specified time
* Option to reboot after a revert
* Option to revert upon command
* Perform tests on configuration files (valid YAML, JSON, TOML, INI and checks file permissions)
* Supports multiple configuration files (not all but it does help catch most issues with many formats)
* Manage testing scenarios with unique names
* Manual control for starting, stopping and removing testing scenarios

> Everything is stored in the `~/.dryrun` directory.
> This directory is created automatically if it does not exist.
> This directory makes it possible manually edit the configuration files and revert to them.

## Installation

```bash
pip install dryrun
```

> Requires Python 3.11 or higher.

> It also uses poetry.

## Usage

```bash
./dryrun.py setup --name test-bob --path /etc/bob
# Make your changes to the configuration files in the `~/.dryrun/test-bob/new` directory
./dryrun.py start --name test-bob
# If anything goes wrong it will revert back.
# If you want to revert manually:
./dryrun.py revert --name test-bob
# If you want to remove the testing scenario:
./dryrun.py remove --name test-bob
```

### Stopping a test

```bash
./dryrun.py stop --name test-bob
```

## Options
* `--name, -n` - The name of the dryrun (only alphanumeric, dashes and underscores are allowed).
* `--path, -p` - The path of the files that will be backed up and replaced for testing.
* `--time, -t` - The duration the new files need to be there before replacing them back with the old ones. Default is '5min'.
* `--reboot, -r` - Choose whether to reboot after a revert. Default is false.
* `--strict, -s` - If true, run tests on the files before applying new configuration. Default is true.

## File Structure
Dryrun creates a directory in the home directory named .dryrun. Inside this directory, it creates a folder for each testing scenario with the name given in the --name option.

Inside each testing scenario directory, it creates two more directories: old and new. The old directory contains a backup of the original configuration files, and the new directory is meant for the new configuration files.

## :scroll: Copyright and License

The license for the code and documentation can be found in the [LICENSE](./LICENSE) file.

---

Made in Québec :fleur_de_lis:, Canada 🇨🇦!