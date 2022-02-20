# Untropy

Untropy is a flexible command line tool to manage full stack _polyglot_
projects.

## Features

- Centralized project configuration with multiple environments and deployment
  tiers.
- Powerful plugin system to wrap and configure external tools.
- Cookiecutter based templates auto-configured from the project configuration.
- ...

## Sequence of commands

```console
> untropy init
> untropy plugin add untropy-externaltool
> untropy plugin create untropy-localtool
> untropy cookie project_template -o awesome_microsvc
> untropy wrapper command ...
...
```

## Rationale

Modern software development solutions are made up a fair amount of technologies
and the number of tools involved can get huge. To cite some that are very
common:

- Terraform
- Packer
- Helm
- Kustomize
- Kubectl
- Yarn
- Pip
- Docker
- Vault
- Ansible
- ...

**TODO** Give some examples (Mattermost ?)

The configuration and execution of all these tools generates a lot a
**entropy**, understood as the quantity of information needed to completely
describe the system:

- Configuration files in different formats.
- Bits of information duplicated across tool configuration.
- Mixed scripting languages (shell, python, ...).

To manage this complexity, development teams sometimes code several script based
tools to ease different use cases (CI, command line, ...). Guided by the DRY
principle, they group those disparate tools into one command, managed into one
project.

Soon, this swiss army knife tool becomes a monolith the whole team depends on
but don't wan't to touch. While they are doing independent microservices
otherwise, they need to manage them with one big CI/CD monolith.

Developers and Devops that got on board early continue to add value to the tool
while newbies and haters try at all cost to avoid it.

Untropy is an attempt to have the benefits of sharing a common set of tools and
good practices while avoiding the maintenance nightmare.

Each tool/wrapper can be developped indepently from the others and integrated in
the projects that make use of them.

Untropy leverages the power and maturity of the python ecosystem and some of its
most interesting libraries and tools:

- pip For package and dependency management.
- pipx for keeping the Untropy Python Virtual environment separate from your
  development environment. This is useful when python is used in the project to
  avoid the dependencies version nightmare.
- Pydantic for configuration management.
- Click and Typer for command execution. Adding an existing typer or click based
  command to untropy is done with one command.

## History

Untropy is inspired by Yinn, a tool I created while working at Unowhy. It
started as an Ansible wrapper in shell and became a click based python CLI. More
CI/CD related tools were then integrated into it. The python package ended
containing the Ansible deployment roles of the common services used by different
solutions of the company. As the package was multi-purpose and monolithic, it
was facing a lot of releases. It became really hard to track the changes and to
avoid regressions on client projects.

As it was based on Ansible, it had its versatility and power, in particular in
templating files and wrapping existing tools. But it also had its flaws, like
not being able to run or even being installed on Windows.

## Credits

Inspiration comes from:

### Terraform

Terraform is a _declarative_ tools, not an imperative one as untropy is but it
defines a common interface for _providers_ and _data sources_. With terraform,
as providers are Go compiled programs, if you want to have your own custom
provider, you need to have the Go runtime installed, build your provider and
upload it to hashicorp public registry or hashicorp cloud private one. It's
uneasy to have a custom provider along your project. With Untropy, as python is
interpreted, a custom plugin living in your project can be run from your project
source code. You also keep the ability to publish your plugins to the cheese
chop or your private repository.

The drawbacks are of course the need for the python runtime and the possible
uncompatibility of libraries used by different plugins.

Composition with Terraform is also uneasy, needing some external tools like
Terragrunt.

### Docker compose

The similarity of untropy with docker compose is that you can _compose_ _Off the
Shelf_ components with custom ones, each of them configured according to the use
you make of them.

In Untropy, the _Off The Shelf_ components would be the Pypi plugins that you
use, and the custom ones are the ones you have in source code form in your
project or the ones you download from a private package registry. As with
docker-compose, you can configure each component (plugin) to your need.

Docker is both the build tool and the runtime execution tools. With untropy and
python, you have the same way or working.
