import urllib.parse as parse

import click
from click._compat import get_text_stderr


class Exception(click.ClickException):
    def show(self, file=None):
        if file is None:
            file = get_text_stderr()
        click.secho("➤➤➤ ", fg="red", bold=True, nl=False, file=file)
        click.echo("Error: {}".format(self.format_message()), file=file)


def log(message: str, error=False, **kwargs):
    click.secho("➤➤➤ ", fg="red" if error else "green", bold=True, nl=False)
    click.secho(message, bold=error, **kwargs)


def warn(message: str, **kwargs):
    click.secho("➤➤➤ ", fg="magenta", bold=True, nl=False)
    click.secho(message, bold=True, **kwargs)


def fail(message: str):
    raise Exception(message)


def progress(message: str, **kwargs):
    click.secho("\r➤➤➤ ", fg="green", bold=True, nl=False)
    click.secho(message, nl=False, **kwargs)
    click.echo("\033[K", nl=False)


def redacted_url(mqtt_url: str) -> str:
    parsed_url = parse.urlparse(mqtt_url)

    replaced = parsed_url._replace(netloc="{}:{}@{}".format(parsed_url.username, "???", parsed_url.hostname))
    return replaced.geturl()
