"""Log View class

This file provides log routing view class and contains the following

Classes:

    * LogView
"""

import logging

from aiohttp.web import Response, Request

from image_converter.settings import config
from image_converter.logger import LOG_PATH
from image_converter.backend.views.decorators import request_log, auth
from image_converter.backend.views.log.logic import GetLogic


log = logging.getLogger(config['project']['name'])


class LogView:
    """
    A class that represent log routes handlers

    Fields
    ----------
    log_path : str
        Path to log file

    Methods
    -------
    get(self, request: Request) -> Response
        Read and return data contains in log file
    """
    log_path = LOG_PATH

    @request_log
    @auth
    async def get(self, request: Request) -> Response:
        """Coroutine handler for log get request

        Parameters
        ----------
        request : Request
            Client request

        Returns
        -------
        Response
            Response for user's request
        """
        logic = GetLogic(request, log, self.get.__name__, self.log_path)
        return await logic.create_stream()
