from assertpy import assert_that
from click.testing import CliRunner

from yat.__main__ import generate

RUNNER = CliRunner()


def test_list_help():
    # arrange & act
    response = RUNNER.invoke(generate,
                             args=[
                                 "--help"
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "Usage: generate [OPTIONS]\n\n"
        "  🏭️ Generate templates for CI/CD platforms.\n\n"
        "Options:\n"
        "  --help  Show this message and exit.\n"
    )
