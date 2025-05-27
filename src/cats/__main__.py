import logging

import uvicorn
from asgi_monitor.logging.uvicorn import build_uvicorn_log_config

from cats.bootstrap import setup_configs
from cats.web import create_app_production

if __name__ == "__main__":
    asgi_conf = setup_configs().asgi
    log_config = build_uvicorn_log_config(
        level=logging.INFO,
        json_format=True,
        include_trace=True,
    )
    uvicorn.run(
        create_app_production(),
        host=asgi_conf.host,
        port=asgi_conf.port,
        log_config=log_config,
    )
