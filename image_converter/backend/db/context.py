"""Database context for aiohttp

This file provides context for aiohttp app

    Coroutines:

        * context(app) - Context coroutine
"""

import asyncio

from image_converter.backend.db.settings import ASYNC_SESSION


async def context(app):
    """Context coroutine run when app run and stop

    Parameters
    ----------
    app : aihttp.web.Application
        aiohttp application

    """
    app['db'] = ASYNC_SESSION()
    yield
    await app['db'].close()
    await asyncio.sleep(.25)
