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

import click

from ..config.model import UntropySettings
from .cli import cli, pass_untropy_settings

ALIAS_LIST = {
    "yd": "cd `untropy home`",
    "yclear": "eval `untropy env -c`",
    "yunalias": "eval `untropy alias --unalias`",
    "yalias": "eval `untropy alias`",
}


ALIASES = "\n".join(f"alias {alias}='{command}'" for (alias, command) in ALIAS_LIST.items())


UNALIAS = "\n".join(f"alias {alias} >/dev/null 2>&1 && unalias {alias}" for alias in ALIAS_LIST.keys())

SCRIPTS = """
function yenv() {
    eval $(untropy env $@)
}

function yd() {
    cd $(untropy home)
}

function yunalias() {
    source <(untropy alias --unalias)
}

function yclear() {
    yenv -c
    yunalias
}

function yalias() {
    source <(untropy alias)
}
"""

UNSCRIPTS = """
{0} yenv
{0} yd
{0} yunalias
{0} yclear
{0} yalias
"""


@cli.command("alias")
@click.option("-u", "--unalias", is_flag=True, help="Remove aliases")
@pass_untropy_settings
def alias(settings: UntropySettings, unalias: bool):
    """Displays the command aliases.

    To define the aliases, type:

    > eval $(untropy alias)

    Then you can reload them with the alias:

    > yalias

    And uninstall them with:

    > yunalias
    """
    # click.echo(UNALIAS if unalias else ALIASES)
    if unalias:
        click.echo(UNSCRIPTS.format("unfunction" if settings.is_zsh_shell else "unset -f"))
    else:
        click.echo(SCRIPTS)


@cli.command("home")
@pass_untropy_settings
def home(settings: UntropySettings):
    """Returns the home directory."""
    click.echo(settings.home)
