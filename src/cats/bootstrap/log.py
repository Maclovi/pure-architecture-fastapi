import logging
import sys

import orjson
from pythonjsonlogger.json import JsonFormatter


def setup_logger() -> None:
    fmt = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"
    formatter = JsonFormatter(fmt, json_serializer=orjson.dumps)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
