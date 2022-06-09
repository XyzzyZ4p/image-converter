"""Image View post logic

This file provides image view logic class for post requests and contains the following

Classes:

    * PostLogic
"""

import asyncio
from logging import Logger
from http import HTTPStatus
from typing import Tuple, Union, Dict

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.decl_api import DeclarativeMeta
from aiohttp import MultipartReader
from aiohttp.web import Response, Request

from image_converter.backend.views.helpers import make_log, create_descriptive_response
from image_converter.backend.views.image.logic.post.helpers import read_multipart_data, process_params
from image_converter.backend.models import Image


class PostLogic:
    """
    A class that represent log view post request processing logic

    Attributes
    ----------
    request : Request
        User's request
    extra : Dict
        Log formatting extra's dict
    db_session : Session
        Open database session
    logger : Logger
        Instance for logger
    allowed_file_formats: Tuple
        Allowed file's mimetypes
    data_keys : Tuple
        Requests parameters keys for image processing
    converter: ImageConverter
        Converter for image processing

    Methods
    -------
    get_multipart_reader(self) -> Union[Response, MultipartReader]
        Initialize multipart connection
    process_data(self, reader: MultipartReader) -> Union[Tuple[Dict, bytes], Response]
        Get data from multipart request
    check_data_content(self, data: bytes) -> Union[bytes, Response]
        Check data contains content
    check_data_params(self, data: Dict) -> Tuple[int, int, int]
        Get params from request body
    add_data_to_db(self, entity: DeclarativeMeta) -> Union[Image, Response]
        Create image in database
    rollback_db(self, data: Image) -> Response
        Rollback for database if error occurred while processing image
    create_image_processing_task(self, data: Image, _bytes: bytes, *args) -> Response:
        Create async task for image processing
    """
    def __init__(self, request: Request,
                 logger: Logger,
                 function_name: str,
                 mimetypes: Tuple,
                 keys: Tuple):

        self.request = request
        self.extra = {'route': request.url, 'functionName': function_name}
        self.db_session = self.request.app['db']
        self.path = self.request.app['settings']['images_path']
        self.logger = logger
        self.allowed_file_formats = mimetypes
        self.data_keys = keys
        self.converter = self.request.app['Converter']

    async def get_multipart_reader(self) -> Union[Response, MultipartReader]:
        """Initialize multipart connection

        Returns
        -------
        Response | MultipartReaderResponse
            Response if error occurs or request reader
        """
        try:
            reader = await self.request.multipart()
        except AssertionError:
            make_log(self.logger,
                     'debug',
                     f'Wrong request Header: Content-Type',
                     self.extra)
            return create_descriptive_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        else:
            return reader

    async def process_data(self, reader: MultipartReader) -> Union[Tuple[Dict, bytes], Response]:
        """Read data from multipart connection

        Parameters
        ----------
        reader : MultipartReader
            Reader for multipart connection

        Returns
        -------
        Response | MultipartReaderResponse
            Response if error occurs or request reader
        """
        try:
            params, _bytes = await read_multipart_data(reader, self.allowed_file_formats)
        except Exception as e:
            make_log(self.logger,
                     'debug',
                     f'Errors in headers processing',
                     self.extra)

            make_log(self.logger,
                     'warning',
                     f'Throws exception: {e.__class__.__name__}',
                     self.extra)

            return create_descriptive_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        else:
            return params, _bytes

    async def check_data_content(self, data: bytes) -> Union[bytes, Response]:
        """Check receive data content

        Parameters
        ----------
        data : bytes
            Data in bytes

        Returns
        -------
        bytes | Response
            Bytes or Response if error occurs
        """
        if not data:
            make_log(self.logger,
                     'debug',
                     f'Empty file data provided',
                     self.extra)

            return create_descriptive_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        return data

    async def check_data_params(self, data: Dict) -> Tuple[int, int, int]:
        """Check received parameters

        Parameters
        ----------
        data : Dict
            Request parameters

        Returns
        -------
        Tuple[int, int, int]
            Tuple contains quality, x, y
        """
        quality, x, y = process_params(data, self.data_keys)
        return quality, x, y

    async def add_data_to_db(self, entity: DeclarativeMeta) -> Union[Image, Response]:
        """Add data to database

        Parameters
        ----------
        entity : DeclarativeMeta
            Database ORM class

        Returns
        -------
        Image | Response
            Image entity or Response if error occurs
        """
        try:
            data = entity()
            self.db_session.add(data)
            await self.db_session.flush()
            await self.db_session.refresh(data)
            _id = str(data.id)
        except Exception as e:
            make_log(self.logger,
                     'error',
                     f'Throws exception while ORM processing: {e.__class__.__name__}',
                     self.extra)
            return create_descriptive_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            return data

    async def rollback_db(self, data: Image) -> Response:
        """Rollback for database if error occurred while processing image

        Parameters
        ----------
        data : DeclarativeMeta instance
            Database ORM entity

        Returns
        -------
        Response
            Server Response
        """
        try:
            await self.db_session.delete(data)
            await self.db_session.flush()
        except DBAPIError:
            make_log(self.logger,
                     'critical',
                     f'Exception occurred while deleting DB entity Image with uuid {data.id}',
                     self.extra)
            return create_descriptive_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            make_log(self.logger,
                     'debug',
                     f'DB entity Image with uuid {data.id} deleted',
                     self.extra)
            return create_descriptive_response(HTTPStatus.UNPROCESSABLE_ENTITY)

    async def create_image_processing_task(self, data: Image, _bytes: bytes, *args) -> Response:
        """Create async task for image processing

        Parameters
        ----------
        data : DeclarativeMeta instance
            Database ORM entity
        _bytes: bytes
            Image coded in bytes
        args: List
            quality, x, y params

        Returns
        -------
        Response
            Server Response
        """
        try:
            await asyncio.create_task(
                self.converter.async_image_process(_bytes, data.id, *args))
        except Exception as e:
            make_log(self.logger,
                     'error',
                     f'Throws exception while Image converting: {e.__class__.__name__}',
                     self.extra)
            return await self.rollback_db(data)
        else:
            return Response(status=HTTPStatus.OK, body=str(data.id))
