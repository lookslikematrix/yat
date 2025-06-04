from assertpy import assert_that
from click.testing import CliRunner

from yat.__main__ import yat

RUNNER = CliRunner()


def test_yat_help():
    # arrange & act
    response = RUNNER.invoke(yat,
                             args=[
                                 "--help"
                             ])

    # assert
    assert_that(response.exit_code).is_equal_to(0)
    assert_that(response.output).is_equal_to(
        "Usage: yat [OPTIONS] COMMAND [ARGS]...\n\n"
        "  🔥 YaT - Command-line interface\n\n"
        "Options:\n"
        "  --loglevel TEXT  Set loglevel.  [default: WARNING]\n"
        "  --help           Show this message and exit.\n"
    )
