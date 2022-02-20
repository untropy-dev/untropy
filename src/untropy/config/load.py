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
from pathlib import Path
from typing import IO, Any, MutableMapping, Optional

import click
import toml
from dotenv import find_dotenv

from .model import UntropySettings

logger = logging.getLogger("untropy")


def find_configuration_file(directory: Path, filename: str = "untropy.toml") -> Optional[Path]:
    directory = directory.resolve()
    path = directory / filename

    logger.debug(f"testing config path: {path}")
    if path.exists():
        return path
    elif directory.parent == directory:
        return None
    else:
        return find_configuration_file(directory.parent, filename)


def load_settings(path: Path, file: Optional[IO[str]] = None) -> MutableMapping[str, Any]:
    settings_dict = toml.load(file or path)
    settings_dict["home"] = str(path.parent)
    settings_dict["settings_filename"] = path.name
    return settings_dict


def load_configuration(directory: Optional[Path] = None) -> UntropySettings:
    static_file_name = "untropy.toml"
    if directory is None:
        path = find_configuration_file(Path("."), static_file_name)
        home = os.getenv("UNTROPY_HOME")
        if home is not None:
            if path is None:
                path = find_configuration_file(Path(home), static_file_name)
            elif str(path.parent) != home:
                raise click.ClickException(
                    f"UNTROPY_HOME ({home}) does not match "
                    f"location of settings file ({path.parent})."
                    " Run 'cd ${UNTROPY_HOME} && eval $(untropy env -c) && cd -' first"
                )
    else:
        path = find_configuration_file(directory, static_file_name)
    try:
        settings_dict = load_settings(path) if path is not None else {}
    except PermissionError:
        raise click.ClickException(f"{path} rights ({oct(os.stat(path).st_mode)[-3:]}) are not enough")
    settings = UntropySettings(find_dotenv(".untropy", usecwd=True), None, **settings_dict)  # type: ignore
    return settings


def load_configuration_file(file: IO[str], path: Path) -> UntropySettings:
    settings_dict = load_settings(path, file)
    return UntropySettings(find_dotenv(".untropy", usecwd=True), None, **settings_dict)  # type: ignore
