"""Setup settings

This file provides setup initializer and contains:
    Constants:
        * PROJECT_ROOT - Root of the project
        * CONFIG_PATH - Path to config path
        * ENCODING = Encoding for log config file

    Functions:

        * get_config(path) -> None
            setup project

    Variables:

        * config - Dict of configs
"""

from pathlib import Path
from yaml import safe_load


PROJECT_ROOT = Path(__file__).parents[1]
CONFIG_PATH = PROJECT_ROOT / 'config' / 'settings.yaml'
ENCODING = 'utf-8'


def get_config(path):
    """Setup project

    Parameters
    ----------
    path : path to config

    Returns
    -------
    dict of config values
    """
    with open(path, encoding=ENCODING) as fp:
        settings = safe_load(fp)

    settings['project_root'] = PROJECT_ROOT
    settings['images_path'] = settings['project_root'] / settings['images']['path']

    return settings


config = get_config(CONFIG_PATH)
