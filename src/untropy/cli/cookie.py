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

import site
import sys
from pathlib import Path

import click
from cookiecutter.main import cookiecutter

from ..config.model import UntropySettings
from ..utils.log import fail
from .cli import cli, pass_untropy_settings

COOKIES_DIR_NAME = "cookies"

COOKIES_DIR_PATH_ELEMENTS = (
    "share",
    "untropy",
    "cookies",
)

COOKIES_DIR_POSSIBLE_PATHS = (
    Path(__file__).parents[3].joinpath(COOKIES_DIR_NAME),  # development
    Path(sys.prefix).joinpath(*COOKIES_DIR_PATH_ELEMENTS),  # standard (venv or base)
    Path(site.getuserbase()).joinpath(*COOKIES_DIR_PATH_ELEMENTS),  # user installation (pip --user)
)

LOCAL_COOKIES_DIR = next((path for path in COOKIES_DIR_POSSIBLE_PATHS if path.exists()), COOKIES_DIR_POSSIBLE_PATHS[1])


def cookie_names():
    return sorted(
        set([str(item.name) for item in LOCAL_COOKIES_DIR.iterdir() if item.is_dir() and not item.name[0] in "_."])
    )


@cli.command("cookie")
@click.option("-l", "--list", is_flag=True, help="List avaible cookie cutters")
@click.option(
    "-O",
    "--output-dir",
    type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    default=".",
    help="Output directory",
)
@click.option("-r", "--replay", is_flag=True, help="Replay the last generation")
@click.option("-o", "--overwrite", is_flag=True, help="Overwrite existing files")
@click.argument("cookie", required=False, default="")
@pass_untropy_settings
def cookie(settings: UntropySettings, list: bool, output_dir: str, replay: bool, overwrite: bool, cookie: str):
    """Install specified COOKIE."""
    if list:
        click.echo("\n".join(cookie_names()))
    else:
        if not cookie:
            fail("A cookie needs to be specified")

        cookiecutter(
            str(LOCAL_COOKIES_DIR),
            directory=cookie,
            output_dir=output_dir,
            extra_context=settings.cookiecutter if not replay else None,
            replay=replay,
            overwrite_if_exists=overwrite,
        )
