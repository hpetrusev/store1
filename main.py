from runner import Runner
import sys
from logs import setup_logging
import logging

setup_logging()
if __name__ == "__main__":
    logging.info(sys.argv[1:])
    if len(sys.argv) > 1:
        runner = Runner(sys.argv[1:])
        runner.run()
    else:
        logging.info("no arguments")
