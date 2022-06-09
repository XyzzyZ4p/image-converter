"""Entrypoint
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from aiohttp.web import Application, run_app

# from image_converter.policy import setup_policies
from image_converter.settings import config
from image_converter.backend.routes import setup_routes
from image_converter.images.converter import ImageConverter
from image_converter.backend.db import context
from image_converter.logger import setup_logging

# setup_policies()
app = Application()
setup_routes(app)
setup_logging()

app.cleanup_ctx.append(context)
app['settings'] = {k: v for k, v in config.items()}
app['Converter'] = ImageConverter(app['settings'])


if __name__ == '__main__':
    run_app(app, host=config['app']['host'], port=config['app']['port'])
