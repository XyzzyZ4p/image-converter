"""Image converter
"""

import asyncio
import concurrent.futures
from io import BytesIO
from functools import partial
from typing import Dict

from PIL import Image


class ImageConverter:
    """
    A class used for image converting

    Attributes
    ----------
    settings : Dict
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
    def __init__(self, settings: Dict):
        self.path = settings['images_path']
        self.format = settings['images']['format']
        self.extension = settings['images']['extension']
        self.compress_method = Image.Resampling.LANCZOS

    def save(self, image: Image, filename: str, quality: int = None) -> None:
        """
        Parameters
        ----------
        image : Image
            PIL.Image
        filename : str
            Path to output file
        quality : int
            Compression quality in %
        """
        if quality:
            image.save(self.path / f'{filename}.{self.extension}', quality=quality, optimize=True)
        else:
            image.save(self.path / f'{filename}.{self.extension}')

    def convert(self, image: Image) -> Image:
        """
        Parameters
        ----------
        image : Image
            PIL.Image

        Returns
        -------
        PIL.Image
            Converted image
        """
        if image.format != self.format:
            return image.convert('RGB')
        return image

    def compress(self, image: Image, x: int, y: int) -> Image:
        """
        Parameters
        ----------
        image : Image
            PIL.Image
        x: int
            Width
        y: int
            Height

        Returns
        -------
        PIL.Image
            Compressed image
        """
        image = image.resize((x, y), self.compress_method)
        return image

    def process(self, _bytes: bytes,
                filename: str,
                quality: int = None,
                x: int = None,
                y: int = None) -> None:

        with BytesIO(_bytes) as buf:
            image = Image.open(buf)
            image = self.convert(image)

            if quality and x and y:
                image = self.compress(image, x, y)
                self.save(image, filename, quality=quality)
            else:
                self.save(image, filename)

    async def async_image_process(self, _bytes: bytes,
                                  filename: str,
                                  quality: int = None,
                                  x: int = None,
                                  y: int = None) -> None:
        """
        Parameters
        ----------
        _bytes : bytes
            Data in bytes
        filename: str
            Output path to file
        quality: int
            Compression quality in %
        x: int
            Width
        y: int
            Height
        """

        loop = asyncio.get_running_loop()

        with concurrent.futures.ProcessPoolExecutor() as pool:
            return await loop.run_in_executor(pool, partial(self.process, _bytes, filename, quality, x, y))
