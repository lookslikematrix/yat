from pathlib import Path
from subprocess import CalledProcessError

import logging
import os
import subprocess
import sys

import click

@click.group()
@click.option(
    "--loglevel",
    help="Set loglevel.",
    default="WARNING",
    show_default=True
)
def yat(loglevel):
    """
    🔥 YaT - Command-line interface
    """
    if loglevel:
        logging.basicConfig(format='%(message)s', encoding='utf-8', level=loglevel)
    else:
        logging.disable(logging.CRITICAL)


@yat.command()
def list():
    """
    📄 List available YaT stages.
    """
    click.echo("pre-commit")


@yat.command()
@click.argument(
    "stage"
)
def run(stage):
    """
    🏎️ Run YaT stage.
    """
    if stage != "pre-commit":
        click.echo(f"[ {stage} ] YaT could not find this stage. Execute `yat list` to get available stages.")
        exit(1)

    script = Path(os.path.realpath(__file__))
    yat_root_directory = Path(os.path.dirname(script)).parent.parent
    subprocess.run(
        [
            "docker",
            "buildx",
            "bake",
            f"yat-{stage}"
        ],
        cwd=yat_root_directory,
        check=True
    )
    current_working_directory = os.getcwd()

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--user",
                f"{os.getuid()}:{os.getgid()}",
                "--volume",
                f"{current_working_directory}:{current_working_directory}",
                "--workdir",
                current_working_directory,
                f"lookslikematrix/yat-{stage}:latest"
            ],
            check=True
        )
    except CalledProcessError:
        sys.exit(1)


if __name__ == '__main__':
    yat()
