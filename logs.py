import logging
import sys
import variables


def setup_logging():
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)-9s [%(filename)s:%(lineno)d]: %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=getattr(logging, variables.LOGLEVEL),
        stream=sys.stdout,
    )
