# coding: utf-8

import os

from msconsparser.adapters.inbound.rest.impl.health_check_filters import HealthEndpointsFilter

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S%z",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "filters": {"health_endpoints_filter": {"()": HealthEndpointsFilter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "DEBUG",
            "filters": ["health_endpoints_filter"],
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["console"]},
        "numba": {"level": "INFO", "handlers": ["console"]},
        "httpcore.http11": {"level": "INFO", "handlers": ["console"]},
    },
}

LOGGING_CONFIG_LOCAL = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "format": ("%(levelname)s:%(name)s:%(message)s"),
        }
    },
    "filters": {"health_endpoints_filter": {"()": HealthEndpointsFilter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
            "level": "DEBUG",
            "filters": ["health_endpoints_filter"],
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["console"]},
        "numba": {"level": "INFO", "handlers": ["console"]},
        "httpcore.http11": {"level": "INFO", "handlers": ["console"]},
    },
}


def get_logging_config() -> dict:
    log_env = os.getenv("LOGGING_CONFIG")
    if log_env is not None and log_env != "local":
        return LOGGING_CONFIG
    else:
        return LOGGING_CONFIG_LOCAL
