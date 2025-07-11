from pathlib import Path
from shutil import copytree, make_archive, rmtree
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


@yat.command(name="list")
def list_command():
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
    project_yat_path = Path(current_working_directory).joinpath("yat.yml")
    project_yat_yaml = None
    environment_args = []
    if project_yat_path.exists():
        logging.info(f"[ {project_yat_path} ] Load project yat.yml.")
        project_yat_yaml = load_yat_yml(project_yat_path)
        environment_args = get_environment_args(project_yat_yaml["environment"])

    yat_yaml = load_yat_yml(yat_root_directory.joinpath("stages").joinpath(stage).joinpath("yat.yml"))

    output_directory = []
    if "environment" in yat_yaml:
        environment_dict = yat_yaml["environment"]
        if project_yat_yaml:
            environment_dict = yat_yaml["environment"] | project_yat_yaml["environment"]
        environment_args = get_environment_args(environment_dict)

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
        command = [
                "docker",
                "run",
                "--rm",
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
            ]

        logging.info(f"[ {' '.join(command)} ] Execute this command.")
        subprocess.run(
            command,
            check=True
        )
    except CalledProcessError:
        sys.exit(1)


@yat.command()
@click.option(
    "--list",
    "list_flag",
    is_flag=True,
    help="List all targets for executing `yat generate TARGET`."
)
@click.option(
    "--output-directory",
    help="Set output directory."
)
@click.argument(
    "target",
    required=False
)
def generate(list_flag, output_directory, target):
    """
    🏭️ Generate templates for CI/CD platforms.
    """
    script = Path(os.path.realpath(__file__))
    yat_directory = Path(os.path.dirname(script)).parent.parent

    if list_flag:
        for directory in os.listdir(yat_directory):
            jinja_template = yat_directory.joinpath(directory).joinpath("yat.jinja2")
            if jinja_template.exists():
                click.echo(directory)
        return

    output_directory_path = Path(output_directory)
    if not output_directory_path.exists():
        os.mkdir(output_directory_path)

    stages_directory = yat_directory.joinpath("stages")
    cli_directory = yat_directory.joinpath("cli")

    if target == "jenkins":
        resources_directory = output_directory_path.joinpath("resources")
        output_stages_directory = resources_directory.joinpath("stages")
        copytree(stages_directory, output_stages_directory, dirs_exist_ok=True)
        output_cli_directory = resources_directory.joinpath("cli")
        copytree(cli_directory, output_cli_directory, dirs_exist_ok=True)
        yat_archive = resources_directory.joinpath("yat")
        make_archive(yat_archive, "zip", resources_directory)
        rmtree(output_stages_directory)
        rmtree(output_cli_directory)

        vars_directory = output_directory_path.joinpath("vars")
        if not vars_directory.exists():
            os.mkdir(vars_directory)


    if target == "github":
        pass


if __name__ == '__main__':
    yat()
