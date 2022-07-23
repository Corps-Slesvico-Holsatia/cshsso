"""Installation scripts."""

from argparse import ArgumentParser
from logging import DEBUG, INFO, basicConfig, getLogger

from cshsso.config import CONFIG, CONFIG_FILE
from cshsso.orm import MODELS


__all__ = ['setup_db']


DB_SETUP_PARSER = ArgumentParser(description='Setup CSHSSO database.')
DB_SETUP_PARSER.add_argument(
    '-s', '--safe', action='store_true', help='ignore existing database tables'
)
DB_SETUP_PARSER.add_argument(
    '-v', '--verbose', action='store_true', help='be gassy'
)


def setup_db() -> int:
    """Set up the databases."""

    args = DB_SETUP_PARSER.parse_args()
    basicConfig(level=DEBUG if args.verbose else INFO)
    logger = getLogger('cshsso-setup-db')
    CONFIG.read(CONFIG_FILE)

    for model in MODELS:
        try:
            model.create_table(safe=args.safe)
        except Exception as error:
            logger.error(str(error))
            return 1

    return 0
