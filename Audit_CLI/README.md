# Audit CLI

> A Command Line Tool for running audits from the NSO Audit & Remediation Framework

This tool is developed with the click framework.
Follow the instructions below to install and set up the CLI.

# Usage

All commands come with documentation and help functions. To view help use `--help`

# Installation

Git clone the package

Either use a virtual environment or your laptops.

cd to the package `cd Audit_CLI`

Install the package `pip install .`

You should now be able to use the CLI from your terminal:

```cli
usename:Audit_CLI username$ audit_cli --help
Usage: audit_cli [OPTIONS] COMMAND [ARGS]...

  Command Line tool for runnning the NSO Audit Framework. The tool allows
  you to run available audits loaded into NSO. The tool dynamically pulls
  available audits from NSO.

  Specificy Audits follows the format:  --group (the audit container)
  --module (the sub use case to the grouping)

  The tool takes hostname, NSO device group, and csv strings of hostnames
  for device inputs.

Options:
  --help  Show this message and exit.

Commands:
  run_audit     Command to run an audit.
  show_groups   Command to get the current list of audit...
  show_modules  Command to get the current list of modules to...

```

# Set Up

> IMPORTANT

Before running any audit commands please set your credentials for NSO using the set_credentials command.

```
username:src username$ audit_cli set_credentials
Password:
Username: admin

                 .--------.
                | .------. |
               | /        \ |
               | |        | |
              _| |________| |_
            .' |_|        |_| '.
            '._____ ____ _____.'
            |     .'____'.     |
            '.__.'.'    '.'.__.'
            '.__  |  NSO |  __.'
            |   '.'.____.'.'   |
            '.____'.____.'____.'
            '.________________.'

          Your password has been set

```
