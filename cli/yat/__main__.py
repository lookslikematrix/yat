import logging

import click

@click.group()
@click.option(
    "--loglevel",
    help="Set loglevel.",
    default="WARNING",
    show_default=True
)
@click.pass_context
def yat(ctx, loglevel, gpu):
    """
    🔥 YaT - Command-line interface
    """
    if loglevel:
        logging.basicConfig(format='%(message)s', encoding='utf-8', level=loglevel)
    else:
        logging.disable(logging.CRITICAL)


if __name__ == '__main__':
    yat()
