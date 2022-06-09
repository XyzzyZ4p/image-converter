"""Image View get logic

This file provides image view logic class for get requests and contains the following

Classes:

    * GetLogic
"""

from logging import Logger
from http import HTTPStatus
from typing import Union
from pathlib import Path

from sqlalchemy.exc import DBAPIError
from aiohttp.web import Response, Request

from image_converter.backend.views.helpers import make_log, file_sender, create_descriptive_response
from image_converter.backend.views.image.logic.get.helpers import add_extension_to_name
from image_converter.backend.models import Image


class GetLogic:
    """
    A class that represent log view get request processing logic

    Attributes
    ----------
    request : Request
        User's request
    extra : Dict
        Log formatting extra's dict
    db_session : Session
        Open database session
    path : str
        Path to images folder
    extension : str
        Extension for creating file
    logger : Logger
        Instance for logger

    Methods
    -------
    get_request_data_id(self) -> str
        Get image id data from request
    receive_data_from_db(self, entity, _id) -> Union[Response, str]:
        Connect to database and try to receive image by orm
    create_stream(self, _id: str) -> Response:
        Send file to Client
    """

    def __init__(self, request: Request, logger: Logger, function_name: str, extension: str):
        self.request = request
        self.extra = {'route': request.url, 'functionName': function_name}
        self.db_session = self.request.app['db']
        self.path = self.request.app['settings']['images_path']
        self.extension = extension
        self.logger = logger

    def get_request_data_id(self) -> str:
        """Get image id data from request

        Returns
        -------
        str
            Image id request data
        """
        return self.request.match_info.get('image_id')

    async def receive_data_from_db(self, entity: Image, _id: str) -> Union[Response, str]:
        """Connect to database and try to get entity by id

        Parameters
        ----------
        entity : Image
            Reader for multipart connection
        _id : str
            Entity id

        Returns
        -------
        Union[Response, str]:
            Response if error occurs or image id
        """
        try:
            data = await self.db_session.get(entity, _id)
            data_id = data.id
        except DBAPIError:
            make_log(self.logger,
                     'debug',
                     f'DB entity Image with uuid {_id} not found',
                     self.extra)
            return create_descriptive_response(HTTPStatus.NOT_FOUND)
        else:
            return data_id

    async def create_stream(self, _id: str) -> Response:
        """Coroutine for read file and write to stream

        Parameters
        ----------
        _id : str
            Entity id

        Returns
        -------
        Response for user's request
        """
        file_name = add_extension_to_name(self.path, _id, self.extension)
        try:
            if not Path(file_name).is_file():
                raise FileNotFoundError  # TODO: Clear db entry
            data = file_sender(file_path=file_name)
        except FileNotFoundError:
            make_log(self.logger,
                     'error',
                     f'Image file {_id} not found',
                     self.extra)
            return create_descriptive_response(HTTPStatus.NOT_FOUND)
        else:
            headers = {"Content-disposition": f"attachment; filename={file_name}"}
            return Response(status=HTTPStatus.OK, body=data, headers=headers)
