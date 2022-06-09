"""Image view

This file provides view for image and contains the following
classes:

    * ImageView
"""

import logging

from aiohttp.web import Response, Request

from image_converter.settings import config
from image_converter.backend.models import Image
from image_converter.backend.views.decorators import request_log, auth
from image_converter.backend.views.image.logic import GetLogic, PostLogic


log = logging.getLogger(config['project']['name'])


class ImageView:
    """
     A class used for handle requests

     ...

     Fields
     ----------
     images_path : Dict
         Settings for ImageConverter setup.

     Methods
     -------
     save(image: Image, filename: str, quality: int = None) -> None
         Save image file
     convert(self, image: Image) -> Image
         Convert image file to specific format
     compress(self, image: Image, x: int, y: int) -> Image:
         Compress image file to provided resolution
     process(self, _bytes: bytes,
             filename: str,
             quality: int = None,
             x: int = None,
             y: int = None) -> None:
         Process provided byte data with convert compress and save
     async_image_process(self, _bytes: bytes,
                         filename: str,
                         quality: int = None,
                         x: int = None,
                         y: int = None) -> None:
         Create and execute process coroutine
     """
    images_path = config['images_path']
    allowed_file_formats = ('image/gif', 'image/jpeg', 'image/png', 'image/tiff')
    data_keys = ('quality', 'x', 'y')

    @request_log
    @auth
    async def get(self, request: Request) -> Response:
        """Coroutine handler for image get request

        Parameters
        ----------
        request : Request
            Client request

        Returns
        -------
        Response
            Response for user's request
        """
        logic = GetLogic(request, log, self.get.__name__, 'jpg')
        session = request.app['db']
        async with session.begin():
            data_id = logic.get_request_data_id()
            data = await logic.receive_data_from_db(Image, data_id)
            if isinstance(data, Response):
                return data
            return await logic.create_stream(data_id)

    @request_log
    @auth
    async def post(self, request: Request) -> Response:
        """Coroutine handler for image post request

        Parameters
        ----------
        request : Request
            Client request

        Returns
        -------
        Response
            Response for user's request
        """
        logic = PostLogic(request,
                          log, self.post.__name__,
                          self.allowed_file_formats,
                          self.data_keys)

        session = request.app['db']
        async with session.begin():
            reader = await logic.get_multipart_reader()
            if isinstance(reader, Response):
                return reader
            data = await logic.process_data(reader)
            if isinstance(data, Response):
                return data
            params, _bytes = data
            data = await logic.check_data_content(_bytes)
            if isinstance(data, Response):
                return data
            params = await logic.check_data_params(params)
            entity = await logic.add_data_to_db(Image)
            if isinstance(entity, Response):
                return entity
            return await logic.create_image_processing_task(entity, data, *params)
