import pytest

from assertpy import assert_that
from click.testing import CliRunner

from yat.__main__ import generate

RUNNER = CliRunner()


def test_generate_help():
    # arrange & act
    response = RUNNER.invoke(generate,
                             args=[
                                 "--help"
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "Usage: generate [OPTIONS] [TARGET]\n\n"
        "  🏭️ Generate templates for CI/CD platforms.\n\n"
        "Options:\n"
        "  --list                   List all targets for executing `yat generate TARGET`.\n"
        "  --output-directory TEXT  Set output directory.\n"
        "  --help                   Show this message and exit.\n"
    )


def test_generate_list():
    # arrange & act
    response = RUNNER.invoke(generate,
                             args=[
                                "--list"
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "github\n"
        "jenkins\n"
    )


@pytest.mark.parametrize(
        "target_platform,target_directories", [
            (
                "jenkins",
                [
                    "resources",
                    "vars"
                ]
            ),
            (
                "github",
                [
                    "pre-commit",
                    "software-composition-analysis"
                ]
            )
        ]
    )
def test_generate_happy_path(target_platform, target_directories, tmp_path):
    # arrange
    output = tmp_path.joinpath(target_platform)

    # act
    response = RUNNER.invoke(generate,
                             args=[
                                 f"--output-directory={output}",
                                 target_platform
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(output.exists()).is_true()
    for target_directory in target_directories:
        output_directory = output.joinpath(target_directory)
        assert_that(output_directory.exists()).is_true()
