from assertpy import assert_that
from click.testing import CliRunner
from pathlib import Path
from unittest.mock import call

import os
import subprocess

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


def test_run_stage_happy_path(mocker):
    # arrange
    stage_name = "pre-commit"
    run_mock = mocker.patch("subprocess.run")
    script = Path(os.path.realpath(__file__))
    yat_root_directory = Path(os.path.dirname(script)).parent.parent
    current_working_directory = os.getcwd()
    # act
    response = RUNNER.invoke(run,
                             args=[
                                 stage_name
                             ])

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
                    "--workdir",
                    current_working_directory,
                    f"lookslikematrix/yat-{stage_name}:latest"
                ],
                check=True
            )
        ]
    )
