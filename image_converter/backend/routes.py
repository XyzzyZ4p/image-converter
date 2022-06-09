"""Setup server routes

This file provides setup function for server routes and contains the following
functions:

    * setup_routes(app) -> None
        setup routes
"""
from aiohttp import web

from image_converter.backend.views import ImageView, LogView


def setup_routes(app):
    """Setup routes

    Parameters
    ----------
    app : aihttp.web.Application
        aiohttp application

    """
    image_view = ImageView()
    log_view = LogView()

    app.add_routes([web.get('/{image_id}', image_view.get),
                    web.post('/', image_view.post),
                    web.get('/log/', log_view.get)])
