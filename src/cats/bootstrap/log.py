import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def setup_logger() -> None:
    fmt = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"
    formatter = JsonFormatter(fmt)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
