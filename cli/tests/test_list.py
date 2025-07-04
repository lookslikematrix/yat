from assertpy import assert_that
from click.testing import CliRunner

from yat.__main__ import list_command

RUNNER = CliRunner()


def test_list_help():
    # arrange & act
    response = RUNNER.invoke(list_command,
                             args=[
                                 "--help"
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "Usage: list [OPTIONS]\n\n"
        "  📄 List available YaT stages.\n\n"
        "Options:\n"
        "  --help  Show this message and exit.\n"
    )


def test_list_happy_path():
    # arrange & act
    response = RUNNER.invoke(list_command)

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "pre-commit\n"
        "software-composition-analysis\n"
    )
