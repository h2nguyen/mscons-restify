# coding: utf-8

import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def startup_lifespan():
    """
    Async context manager for handling application startup events.

    This function logs when the application starts up and provides a lifespan
    context for the FastAPI application. It's used to perform initialization
    tasks when the application starts.

    Yields:
        None: Control is yielded back to the application after startup
    """
    logger.info("App startup")
    yield
