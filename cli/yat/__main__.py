from pathlib import Path
from subprocess import CalledProcessError

import logging
import os
import subprocess
import sys
import yaml

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
    script = Path(os.path.realpath(__file__))
    yat_root_directory = Path(os.path.dirname(script)).parent.parent
    for directory in sorted(os.listdir(yat_root_directory.joinpath("stages"))):
        click.echo(directory)


def load_yat_yml(yat_yaml_path: Path):
    if not yat_yaml_path.exists():
        return {}

    with open(yat_yaml_path, "r") as file:
        return yaml.safe_load(file)

def get_environment_args(environment_dict):
    environment_args = []

    for environment in environment_dict:
        environment_value = os.getenv(environment, environment_dict[environment])
        if environment_value is None:
            continue

        environment_args.extend([
            "--env",
            f"{environment}={environment_value}"
        ])

    return environment_args

@yat.command()
@click.argument(
    "stage"
)
def run(stage):
    """
    🏎️ Run YaT stage.
    """

    script = Path(os.path.realpath(__file__))
    yat_root_directory = Path(os.path.dirname(script)).parent.parent
    if stage not in os.listdir(yat_root_directory.joinpath("stages")):
        click.echo(f"[ {stage} ] YaT could not find this stage. Execute `yat list` to get available stages.")
        exit(1)

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
    yat_yaml = load_yat_yml(yat_root_directory.joinpath("stages").joinpath(stage).joinpath("yat.yml"))

    environment_args = []
    output_directory = []
    if "environment" in yat_yaml:
        environment_args = get_environment_args(yat_yaml["environment"])

        output_directory_value = os.getenv("YAT_OUTPUT_DIRECTORY")

        if output_directory_value is None:
            if "YAT_OUTPUT_DIRECTORY" in yat_yaml["environment"]:
                output_directory_value = yat_yaml["environment"]["YAT_OUTPUT_DIRECTORY"]

        if output_directory_value:
            output_directory_path = Path(output_directory_value)
            os.makedirs(output_directory_value, exist_ok=True)
            output_directory = [
                "--volume",
                f"{output_directory_path.absolute()}:{output_directory_path.absolute()}"
            ]

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--user",
                f"{os.getuid()}:{os.getgid()}",
                "--volume",
                f"{current_working_directory}:{current_working_directory}",
                *output_directory,
                "--workdir",
                current_working_directory,
                *environment_args,
                f"lookslikematrix/yat-{stage}:latest",
                *yat_yaml["command"]
            ],
            check=True
        )
    except CalledProcessError:
        sys.exit(1)


if __name__ == '__main__':
    yat()
