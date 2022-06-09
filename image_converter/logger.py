"""Setup logging

This file provides setup function for logging module and contains:
    Constants:
        * PROJECT_ROOT - Root of the project
        * LOG_CONFIG_PATH - Path to logging config path
        * LOG_PATH = Log file path
        * ENCODING = Encoding for log config file

    Functions:

        * setup_logging(app) -> None
            setup logging module
"""

import logging
import logging.config
from pathlib import Path

from yaml import safe_load

from image_converter.settings import config


PROJECT_ROOT = Path(__file__).parents[1].resolve()
LOG_CONFIG_PATH = PROJECT_ROOT / 'config' / 'logging.yaml'
LOG_PATH = str(PROJECT_ROOT / config['logging']['path'])
ENCODING = config['project']['encoding']


def setup_logging():
    """Setup logging
    """
    with open(LOG_CONFIG_PATH, encoding=ENCODING) as fp:
        logging_settings = safe_load(fp)

    logging_settings['version'] = 1
    logging_settings['disable_existing_loggers'] = False
    logging_settings['handlers']['file']['filename'] = LOG_PATH
    logging.config.dictConfig(logging_settings)
