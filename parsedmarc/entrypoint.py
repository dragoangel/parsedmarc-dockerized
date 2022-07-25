#!/usr/bin/env python3

from functools import wraps
from pathlib import Path
import os
import sys
from typing import Mapping, Tuple


ConfigValues = Mapping[str, Mapping[str, str]]


# name of executable
APP_NAME = "parsedmarc"
# separator for section and option
ENV_SEPARATOR = "."
# path to config file to generate & overwrite
CONFIG_PATH = "/etc/parsedmarc.conf"
# prefix for env options
ENV_PREFIX = f"{APP_NAME}{ENV_SEPARATOR}"


@wraps(print)
def error(*args, **kwargs):
    ret = print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()
    return ret


def get_env_name(section: str, option: str) -> str:
    return f"{section}_{option}"


def read_config_from_env() -> ConfigValues:
    values: ConfigValues = dict()
    for env_name, env_val in os.environ.items():
        if not env_name.startswith(ENV_PREFIX):
            continue
        env_name = env_name[len(ENV_PREFIX) :]
        section, option = env_name.split(ENV_SEPARATOR, 1)
        if section not in values:
            values[section] = dict()
        values[section][option] = env_val
    return values


def write_config_file(path: os.PathLike, config: ConfigValues) -> None:
    with Path(path).open("w") as fh:
        for section, option_values in config.items():
            fh.write(f"[{section}]\n")
            for option, value in option_values.items():
                fh.write(f"{option} = {value}\n")


def prepare_config() -> bool:
    config_vals = read_config_from_env()
    if config_vals:
        error(f"Read {ENV_PREFIX}* options from environment, write to {CONFIG_PATH}")
        write_config_file(path=CONFIG_PATH, config=config_vals)
        return True
    return False


def main() -> None:
    args = list(sys.argv[1:])
    config_generated = prepare_config()
    if len(args) > 0 and not args[0].startswith("-"):
        # first arg does not look like a normal option, more like an executable
        # should catch cases of "docker run image /bin/bash"
        exec_name = args[0]
        error(f"User requested to execute {exec_name!r} instead of {APP_NAME}")
    else:
        if config_generated:
            error("Append generated config file to arguments")
            args = ["--config-file", CONFIG_PATH] + args
        args = [APP_NAME] + args
    error(f"Execute: {args!r}")
    return os.execvp(args[0], args)


if __name__ == "__main__":
    main()
