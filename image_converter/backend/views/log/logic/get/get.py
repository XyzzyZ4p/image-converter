"""Log View get logic

This file provides log view logic class and contains the following

Classes:

    * GetLogic
"""

from logging import Logger
from http import HTTPStatus
from pathlib import Path

from aiohttp.web import Response, Request

from image_converter.backend.views.helpers import make_log, create_descriptive_response, file_sender


class GetLogic:
    """
    A class that represent log view get request processing logic

    Attributes
    ----------
    request : Request
        User's request
    logger : Logger
        Instance for logger
    function_name : str
        Name of called function
    path: str
        Path to log file

    Methods
    -------
    create_stream(self) -> Response
        Read and return data contains in log file
    """
    def __init__(self, request: Request, logger: Logger, function_name: str, path: str):
        self.request = request
        self.extra = {'route': request.url, 'functionName': function_name}
        self.path = path
        self.logger = logger

    async def create_stream(self) -> Response:
        """Coroutine for read file and write to stream

        Returns
        -------
        Response for user's request
        """
        try:
            if not Path(self.path).is_file():
                raise FileNotFoundError  # TODO: implements method for check
            data = file_sender(file_path=self.path)
        except FileNotFoundError:
            make_log(self.logger,
                     'error',
                     'Log file not found',
                     self.extra)
            return create_descriptive_response(HTTPStatus.NOT_FOUND)
        else:
            headers = {"Content-disposition": f"attachment; filename=log"}
            return Response(status=HTTPStatus.OK, body=data, headers=headers)
