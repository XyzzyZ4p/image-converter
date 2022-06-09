"""Image View post logic helpers

This file provides helper functions to view logic class
for post requests and contains the following

Functions:

    * dict_from_string(data: str) -> Dict
    * process_params(params: Dict, keys: Tuple) -> Tuple:

Coroutines:

    * read_by_chunks(data: Union[MultipartReader, BodyPartReader, None]) -> bytes
    * read_multipart_data(reader: MultipartReader,
                          allowed_file_formats: Tuple) -> Tuple[Dict, bytes]
"""

import re
from io import BytesIO
from typing import Dict, Tuple, Union

from aiohttp import MultipartReader, BodyPartReader
from aiohttp.web import HTTPUnsupportedMediaType
from aiohttp.hdrs import CONTENT_TYPE


def dict_from_string(data: str) -> Dict:
    """Parse params data

    Parameters
    ----------
    data : str
        Received params

    Returns
    -------
    Dict
        Contains received params keys
    """
    metadata = {}
    data = re.sub(r'[{}]', '', data)
    for params in data.split(','):
        k, v = params.split('=')
        metadata[k] = int(v)
    return metadata


def process_params(params: Dict, keys: Tuple) -> Tuple:
    """Get values from parsed params dict

    Parameters
    ----------
    params : Dict
        Params dict
    keys : Tuple
        Searching keys

    Returns
    -------
    Tuple
        Contains required keys
    """
    if params and all(k in params for k in keys):
        try:
            quality = int(params.get('quality'))
            x = int(params.get('x'))
            y = int(params.get('y'))

        except ValueError:
            return None, None, None

        else:
            return quality, x, y

    else:
        return None, None, None


async def read_by_chunks(data: Union[MultipartReader, BodyPartReader, None]) -> bytes:
    """Read chunks of multipart data

    Parameters
    ----------
    data : Union[MultipartReader, BodyPartReader, None]
        Request data

    Returns
    -------
    bytes
        Received data in bytes
    """
    with BytesIO() as buf:
        while True:
            chunk = await data.read_chunk()
            if not chunk:
                break
            buf.write(chunk)
        _bytes = buf.getbuffer().tobytes()
    return _bytes


async def read_multipart_data(reader: MultipartReader,
                              allowed_file_formats: Tuple) -> Tuple[Dict, bytes]:
    """Process multipart data with headers check

        Parameters
        ----------
        reader : MultipartReader
            Reader for multipart data
        allowed_file_formats : Tuple
            Allowed mimetypes

        Returns
        -------
        Tuple[Dict, bytes]
            Received data and params
        """
    params = _bytes = None

    while True:
        part = await reader.next()

        if part is None:
            break

        elif part.headers[CONTENT_TYPE] == 'text/plain':
            data = await part.text()
            params = dict_from_string(data)

        elif part.headers[CONTENT_TYPE] in allowed_file_formats:
            _bytes = await read_by_chunks(part)

        else:
            raise HTTPUnsupportedMediaType

    return params, _bytes
