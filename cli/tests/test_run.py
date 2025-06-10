import pytest

from assertpy import assert_that
from click.testing import CliRunner
from pathlib import Path
from unittest.mock import call

import os

from yat.__main__ import run

RUNNER = CliRunner()


def test_run_help():
    # arrange & act
    response = RUNNER.invoke(run,
                             args=[
                                 "--help"
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "Usage: run [OPTIONS] STAGE\n\n"
        "  🏎️ Run YaT stage.\n\n"
        "Options:\n"
        "  --help  Show this message and exit.\n"
    )


def test_run_stage_do_not_exists():
    # arrange
    stage_name = "do-not-exists"

    # act
    response = RUNNER.invoke(run,
                             args=[
                                 stage_name
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(1)
    assert_that(response.output).is_equal_to(
        f"[ {stage_name} ] YaT could not find this stage. Execute `yat list` to get available stages.\n"
    )

@pytest.mark.parametrize(
        "stage_name,environment_args", [
            (
                "pre-commit",
                [
                    "--env",
                    "TARGET_BRANCH=origin/main"
                ]
            ),
            (
                "software-composition-analysis",
                [
                    "--env",
                    "YAT_OUTPUT_DIRECTORY=output_directory"
                ]
            )
        ]
    )
def test_run_stage_happy_path(mocker, stage_name, environment_args):
    # arrange
    run_mock = mocker.patch("subprocess.run")
    script = Path(os.path.realpath(__file__))
    yat_root_directory = Path(os.path.dirname(script)).parent.parent
    current_working_directory = os.getcwd()
    output_directory = "output_directory"
    output_directory_path = Path(output_directory).absolute()
    # act
    response = RUNNER.invoke(run,
                             args=[
                                 stage_name
                             ],
                             env={
                                 "YAT_OUTPUT_DIRECTORY": output_directory
                             })

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    run_mock.assert_has_calls(
        [
            call(
                [
                    "docker",
                    "buildx",
                    "bake",
                    f"yat-{stage_name}"
                ],
                cwd=yat_root_directory,
                check=True
            ),
            call(
                [
                    "docker",
                    "run",
                    "--user",
                    f"{os.getuid()}:{os.getgid()}",
                    "--volume",
                    f"{current_working_directory}:{current_working_directory}",
                    "--volume",
                    f"{output_directory_path}:{output_directory_path}",
                    "--workdir",
                    current_working_directory,
                    *environment_args,
                    f"lookslikematrix/yat-{stage_name}:latest",
                    "/bin/sh",
                    "/.yat/run.sh"
                ],
                check=True
            )
        ]
    )


@pytest.mark.integration_tests
def test_run_software_composition_analysis(tmp_path):
    # arrange
    stage_name = "software-composition-analysis"
    release_name = "yat"
    release_version = "1.2.3"
    sbom_path = tmp_path.joinpath(f"{release_name}_{release_version}.cyclondx.json")
    script = Path(os.path.realpath(__file__))
    source_directory = Path(os.path.dirname(script)).parent.parent.joinpath("cli")

    # act
    response = RUNNER.invoke(run,
                             args=[
                                 stage_name,
                             ],
                             env={
                                 "SOURCE_DIRECTORY": str(source_directory),
                                 "YAT_RELEASE_NAME": release_name,
                                 "YAT_RELEASE_VERSION": release_version,
                                 "YAT_OUTPUT_DIRECTORY": str(tmp_path)
                             })

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(sbom_path.exists()).is_true()
