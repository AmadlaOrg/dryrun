<a href="https://amadla.org/projects/dryrun/" align="right"><img src="./assets/An_alchemist_in_his_laboratory._Oil_painting_by_a_follower_o_Wellcome_V0017658-450x.webp" alt="dryrun logo" style="width: 450px;" align="right"></a>

# dryrun

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](./README.md)
[![Language: Français](https://img.shields.io/badge/Langue-Fran%C3%A7ais-blue.svg)](./README.fr.md)

[![Python 3.11](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](#)

Dryrun is a Python-based command-line tool designed to automate the process of testing changes to configuration files. It allows you to backup existing configurations, apply new configurations, and revert to the old configurations automatically after a specified duration or upon command.

This tool is particularly useful for scenarios where you need to test changes that may cause a loss of connectivity or have other significant effects, as it allows you to revert to a previous state automatically.

> Ok Ok!! It is not exactly a dry run, but it is close enough! Unless something catastrophic happens (no more network connect plus cron job breaks), you will be able to revert to the old configurations.

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

### Setup a New Test
The `setup` command creates a new testing scenario. It backs up the files from the provided path into an 'old' directory and prepares a 'new' directory for new configurations.
```bash
dryrun setup --name test-bob --path /etc/bob
```

> Make your changes to the configuration files in the `~/.dryrun/test-bob/new` directory.

### Running a test
The `run` command starts a previously set up testing scenario. It applies the new configuration and schedules a revert to the old configuration after the specified time.
```bash
dryrun run --name test-bob
```

### Stopping a test
The `stop` command stops a running test and reverts to the old configuration immediately.
```bash
dryrun stop --name test-bob
```

### Remove a test
The `remove` command removes a testing scenario completely, including its backup files.
```bash
dryrun remove --name test-bob
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
