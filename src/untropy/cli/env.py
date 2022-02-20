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

import json
import logging
import re
from pathlib import PosixPath, WindowsPath
from typing import Any, Literal, Mapping, Optional, Union

import click
import yaml
from pydantic.json import pydantic_encoder

from ..config.model import (
    SHELL_ENVIRONMENT_NAMES,
    UntropyConfigurationError,
    UntropySettings,
)
from ..utils.log import fail, log
from .cli import cli, pass_untropy_settings

logger = logging.getLogger("untropy")


class UntropyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return pydantic_encoder(o)
        except TypeError:
            return super(UntropyJSONEncoder, self).default(o)


def to_json(vars: Mapping[str, Any], indent: int = 2, sort_keys: bool = True, *args, **kw):
    return json.dumps(
        vars, cls=UntropyJSONEncoder, indent=indent, sort_keys=sort_keys, separators=(",", ": "), *args, **kw
    )


def represent_posixpath(dumper, path: Union[PosixPath, WindowsPath]):
    return yaml.representer.SafeRepresenter.represent_str(dumper, str(path))


yaml.Dumper.add_representer(PosixPath, represent_posixpath)
yaml.Dumper.add_representer(WindowsPath, represent_posixpath)


def print_names(settings: UntropySettings):
    for env in settings.environment_names:
        if env == settings.env:
            click.secho("* ", bold=True, fg="red", nl=False)
        else:
            click.secho("  ", nl=False)
        click.echo(env)


ENV_REGEX = re.compile(r'UNTROPY_ENV=.*\n', re.M)


def save_environment(settings: UntropySettings):
    path = settings.env_file
    line = f"UNTROPY_ENV={settings.env}"
    content = line + "\n"

    logger.debug(f"Path of the configuration file: {path}")

    if path.exists():
        content = ENV_REGEX.sub("", path.read_text("utf-8")) + content

    path.write_text(content)


def set_environment(settings: UntropySettings, environment: Optional[str], save: bool = False) -> bool:
    names = settings.environment_names

    if (current_env := environment or settings.env) not in names:
        log(
            f"Error. environment {current_env} doesn't exist! Possible environments:",
            error=True,
        )
        print_names(settings)
        return False

    if environment is not None:
        settings.env = environment
        if save:
            save_environment(settings)

    return True


def clear_env(settings: UntropySettings):
    """Clear environment."""
    template = "set -e {0}" if settings.is_fish_shell else "unset {0}"

    click.echo("\n".join(template.format(key) for key in SHELL_ENVIRONMENT_NAMES))


def set_env(settings: UntropySettings):
    """Set environment."""
    template = "set -x {0} {1}" if settings.is_fish_shell else "export {0}={1}"

    click.echo("\n".join(template.format(key, value) for (key, value) in settings.shell_environment.items()))


def shell_command(settings: UntropySettings, clear: bool) -> str:
    """Return shell command depending on environment."""
    if clear:
        return "untropy env --clear"
    else:
        return f"untropy env {settings.env}"


def eval_command(settings: UntropySettings, clear: bool) -> str:
    """Return command to eval depending on environment."""
    if settings.is_fish_shell:
        return f"{shell_command(settings, clear)} | source"
    else:
        return f"eval $({shell_command(settings, clear)})"


@cli.command("env")
@click.option("-l", "--list", is_flag=True, help="List environments")
@click.option("-s", "--save", is_flag=True, help="Save environment to .untropy")
@click.option("-c", "--clear", is_flag=True, help="Clear environment")
@click.option("--show", is_flag=True, help="Show environment")
@click.option("--format", type=click.Choice(["yaml", "json"]), default="yaml", help="Output format", show_default=True)
@click.argument("environment", type=str, required=False)
@pass_untropy_settings
def env(
    settings: UntropySettings,
    list: bool,
    save: bool,
    clear: bool,
    show: bool,
    format: Literal["yaml", "json"],
    environment: Optional[str],
):
    """Set or retrieve the environment.

    List the environments with:

    > untropy env -l

    To set the environment to ENVIRONMENT, type:

    > eval $(untropy env ENVIRONMENT)

    Use -s to save it as the default. To unset environment variables, type:

    > eval $(untropy env -c)
    """
    if list:
        print_names(settings)
    elif clear:
        clear_env(settings)
        click.echo(
            f"""\
\n# Run this command to clear your shell:
# {eval_command(settings, clear)}\
"""
        )
    elif show:
        if not set_environment(settings, environment):
            return 1
        click.echo_via_pager(yaml.dump(settings.internal_vars) if format == "yaml" else to_json(settings.internal_vars))
    else:
        try:
            if not set_environment(settings, environment, save):
                return 1

            set_env(settings)
            click.echo(
                f"""\
\n# Run this command to configure your shell:
# {eval_command(settings, clear)}\
    """
            )
        except UntropyConfigurationError as e:
            fail(f"Error: {e}")
