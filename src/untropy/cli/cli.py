# Copyright 2022 Antoine Martin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import re
import typing
from importlib.metadata import version
from logging.config import dictConfig
from pathlib import Path

import click
import toml

from ..config import UntropySettings, load_configuration, load_configuration_file
from ..utils.log import fail, log
from ..utils.log_setup import setup_logging

setup_logging()

logger = logging.getLogger("untropy")

SILENT_HANDLERS = ["transitions.core", "urllib3.connectionpool", "openstack"]

pass_untropy_settings = click.make_pass_decorator(UntropySettings)


def force_environment(settings: UntropySettings):
    """Force environment variables from settings."""
    log("Forcing environment variables...")
    for name, value in settings.shell_environment.items():
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"{name}={value}")
        os.putenv(name, value)
        os.environ[name] = str(value)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Force reloading inventory on {settings.env}")


untropy_version = re.compile(r"\.dev\d+$").sub("", version("untropy"))


@click.group("untropy")
@click.version_option(untropy_version)
@click.option("-v", "--verbose", count=True, help="Increase verbosity (repeat)")
@click.option(
    "--log-config",
    type=click.File("r"),
    required=False,
    help="Log configuration (incremental by default)",
)
@click.option(
    "--config",
    type=click.File("r"),
    required=False,
    help="Project configuration file",
)
@click.option("-f", "--force-env", is_flag=True, help="Force the environment variables")
@click.pass_context
def cli(
    context: click.Context,
    verbose,
    log_config: typing.Optional[typing.IO[typing.Text]],
    config: typing.Optional[typing.IO[typing.Text]],
    force_env: bool,
):
    """Untropy - One development tool to rule them all."""
    if verbose > 0:
        root_logger = logging.getLogger()
        current_level = root_logger.level
        level = max(current_level - (verbose * 10), logging.DEBUG)
        click.secho("➤➤➤ ", fg="green", bold=True, nl=False)
        click.secho(
            (
                f"Verbose is {verbose}."
                f" Setting log level from {logging.getLevelName(current_level)} to {logging.getLevelName(level)}..."
            ),
            bold=True,
        )
        root_logger.setLevel(level)
        for handler in root_logger.handlers:
            handler.setLevel(max(handler.level - (verbose * 10), logging.DEBUG))

    if log_config:
        log_additional_config = toml.load(log_config)
        if "incremental" not in log_additional_config:  # Specify false to replace whole configuration
            log_additional_config["incremental"] = True
        log_additional_config["version"] = 1
        dictConfig(log_additional_config)

    for name in SILENT_HANDLERS:
        current_logger = logging.getLogger(name)
        current_logger.disabled = True
        current_logger.propagate = False

    try:
        if config is not None:
            settings = load_configuration_file(config, Path(config.name).resolve())
        else:
            settings = load_configuration()
    except Exception as e:
        fail(str(e))

    if force_env:
        force_environment(settings)

    context.obj = settings
