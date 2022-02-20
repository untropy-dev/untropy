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

import os
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Type,
    TypeVar,
    cast,
    get_args,
)

from dotenv import find_dotenv
from pydantic import BaseSettings, Field, validator

# Deployment tier (see https://en.wikipedia.org/wiki/Deployment_environment)
DeploymentTier = Literal[
    "dev",  # Development
    "test",  # Testing by the QA team
    "ci",  # CI automated deployment and smoke test
    "preprod",  # staging environment (non-regression, performance)
    "prod",  # Production
]


CICommand = Literal[
    "unknown",  # No particular command
    "build",  # Build and unit test
    "package",  # Build docker image, python package, ...
    "publish",  # Publish package
    "deploy",  # Deploy exsting published versioned item in Deployment tier
    "alldeploy",  # Package, publish and deploy
]

SHELL_ENVIRONMENT_NAMES = {
    "OBJC_DISABLE_INITIALIZE_FORK_SAFETY",
    "UNTROPY_ENV",
    "UNTROPY_HOME",
    "UNTROPY_WORKSPACE",
    "UNTROPY_DOMAIN_PREFIX",
    "UNTROPY_DOMAIN_NAME",
    "DOCKER_IMAGE_TAG",
}

UNTROPY_CLOUD_GROUP_NAME = "untropycloud"
UNTROPY_VM_GROUP_NAME = "untropyvm"


class UntropyConfigurationError(Exception):
    pass


class UntropyBaseSettings(BaseSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(find_dotenv(".untropy", usecwd=True), None, **kwargs)  # type: ignore


class DomainSettings(UntropyBaseSettings):
    """Domain related configuration."""

    suffix: str = "untropy.dev"
    local_prefixes: List[str] = [
        "local",
        "local-registry",
        "local-grafana",
        "local-kube",
    ]

    class Config:
        env_prefix = "UNTROPY_DOMAIN_"


class KeySettings(UntropyBaseSettings):
    """Keys related configuration."""

    ssh: Optional[str] = None
    gpg: Optional[Dict[str, List[str]]] = None

    class Config:
        env_prefix = "UNTROPY_KEY_"


LT = TypeVar("LT")


def check_literal(candidate: str, literal: Type[LT]) -> LT:
    if candidate not in get_args(literal):
        raise ValueError((f"Bad value for: {candidate}. " f"Possible values: {', '.join(get_args(literal))}"))
    return cast(LT, candidate)


class UntropyEnvironment:
    """Environment to target.

    An Untropy environment is composed of a project and a Tier. Environments can
    be provided by plugins or specified in the projet `untropy.toml` or
    `pyproject.toml` file.

    It is expressed in the `UNTROPY_ENV` environment variable as
    `<project>_<tier>`, i.e. `untropy_dev`.
    """

    project: str
    "The project name of the environment"

    tier: DeploymentTier
    "The tier of the environment"

    def __init__(self, env: str) -> None:
        self.project, tier_candidate = env.split("_")
        self.tier = check_literal(tier_candidate, DeploymentTier)  # type: ignore

    def __str__(self) -> str:
        return f"{self.project}_{self.tier}"

    @property
    def groups(self) -> List[str]:
        return [self.tier, self.project, str(self)]

    @property
    def cloud_name(self) -> str:
        return f"cloud_{self}"

    @property
    def hyperdev_name(self) -> str:
        return f"hyperdev_{self.project}_dev"


class UntropyCISettings(BaseSettings):
    """Basic CI settings."""

    command: CICommand = "unknown"
    service: Optional[str]
    env: Optional[str]

    def tags(self, tags: Optional[List[str]]) -> List[str]:
        tags = tags or []
        if self.command == "package":
            tags.append("build_image")
        return tags

    def extra_vars(self, extra_vars: Optional[Iterable[str]]) -> List[str]:
        extra_vars = list(extra_vars or [])
        if self.command in ["package", "publish", "deploy", "alldeploy"]:
            extra_vars.append("build_image=yes")
        return extra_vars


class UntropySettings(BaseSettings):
    home: Path = Path(".").absolute()
    settings_filename: str = "untropy.toml"
    env: str = "devops_dev"
    suffix: str = ".yaml"
    ci_settings: UntropyCISettings = Field(default_factory=UntropyCISettings)
    ci_commit_tag: Optional[str] = Field(None, env="CI_COMMIT_TAG")

    domain: DomainSettings = Field(default_factory=DomainSettings)
    credentials: KeySettings = Field(default_factory=KeySettings)
    variables: Optional[Dict[str, str]]
    workspace: Path = Path("~/.untropy").expanduser()
    cookiecutter: Optional[Dict[str, str]]
    secrets_file: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.ci_commit_tag is not None:
            components = self.ci_commit_tag.split("/")
            self.ci_settings.command = check_literal(components[0], CICommand)  # type: ignore
            self.ci_settings.service = components[1] if len(components) > 1 else None
            self.ci_settings.env = components[2] if len(components) > 2 else None
            if self.ci_settings.env:
                self.env = self.ci_settings.env

    @validator("env")
    def env_should_be_splittable(cls, v):
        if "_" not in v or len(v.split("_")) != 2:
            raise ValueError(f"Environment name [{v}] is not in the form <platform>_<tier>, i.e. devops_dev.")
        return v

    @property
    def untropy_env(self) -> UntropyEnvironment:
        return UntropyEnvironment(self.env)

    @property
    def shell_environment(self) -> Dict[str, str]:
        result = {
            "OBJC_DISABLE_INITIALIZE_FORK_SAFETY": "YES",
            "UNTROPY_ENV": self.env,
            "UNTROPY_PROJECT": self.untropy_env.project,
            "UNTROPY_TIER": self.untropy_env.tier,
            "UNTROPY_HOME": str(self.home),
            "UNTROPY_WORKSPACE": str(self.workspace),
            "DOCKER_IMAGE_TAG": self.env.split("_")[-1],
        }
        if self.variables:
            # TODO: should template variables
            result.update(self.variables)

        return result

    @property
    def is_fish_shell(self) -> bool:
        return "fish" in os.getenv("SHELL", "")

    @property
    def is_zsh_shell(self) -> bool:
        return "zsh" in os.getenv("SHELL", "")

    @property
    def internal_vars(self) -> Mapping[str, Any]:
        # FIXME: better output
        return self.dict(exclude_none=True)

    @property
    def environment_names(self) -> List[str]:
        # FIXME: Where do I get those ?
        return [self.env]

    @property
    def ssh_private_key_file(self) -> Optional[str]:
        return str(Path(f"~/.ssh/{self.credentials.ssh}").expanduser()) if self.credentials.ssh else None

    @property
    def env_file(self) -> Path:
        return self.home / ".untropy"

    def ssh_command(self, host: str) -> List[str]:
        command = ["ssh"]
        key = self.ssh_private_key_file
        if key:
            command.append("-i")
            command.append(key)
        command.append(f"arch@{host}")
        return command

    class Config:
        env_prefix = "untropy_"
        env_file = ".untropy"
