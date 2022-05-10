import logging
import logging.config
import os

import click
import toml

DEFAULT_CONFIGURATION = """
version = 1
disable_existing_loggers = false

[formatters.verbose]
class = "coloredlogs.ColoredFormatter"
format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
datefmt = "%H:%M:%S"

[formatters.server]
class = "coloredlogs.ColoredFormatter"
datefmt = "%Y-%m-%dT%H:%M:%S%z"
format = "%(asctime)s %(message)s"

[formatters.simple]
format = "%(message)s"

[handlers.console]
level = "DEBUG"
formatter = "verbose"
class = "logging.StreamHandler"

[handlers.httplog]
level = "INFO"
formatter = "server"
class = "logging.StreamHandler"

[loggers.server]
level = "INFO"
propagate = false
handlers = [ "httplog"]

[root]
handlers = [ "console" ]
level = "WARNING"
"""


def setup_logging(default_path="log_config.toml", env_key="LOG_CONFIG"):
    path = os.getenv(env_key, default_path)
    configured = False
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = toml.load(f)
                logging.config.dictConfig(config)
                configured = True
            except Exception as error:
                click.secho("➤➤➤ ", fg="red", bold=True, nl=False)
                click.secho(
                    f"Error in Logging Configuration ({error}). Using default configuration.",
                    bold=True,
                )
    if not configured:
        logging.config.dictConfig(toml.loads(DEFAULT_CONFIGURATION))
