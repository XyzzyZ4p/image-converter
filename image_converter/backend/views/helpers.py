"""Utility tools for views

This file provides functions that can be called by view and contains the following
functions:

    * make_log(logger: Logger,
               level: str,
               msg: str,
               extra:
               Dict) -> None:
        Log data with provided msg
    * create_code_description(status_code: int) -> str:
        Format msg with server response status description
    * create_descriptive_response(status: int) -> Response:
        Create response with specific status and status description
    * file_sender(writer, file_path=None)
        Create asynchronous write stream for read file
"""

import asyncio
from logging import Logger
from http.client import responses
from typing import Dict
from pathlib import Path


from aiohttp import streamer
from aiohttp.web import Response


def make_log(logger: Logger, level: str, msg: str, extra: Dict) -> None:
    """Write to log handler

    Parameters
    ----------
    logger : Logger with extra provided data
    level: Log level
    msg: Logging message
    extra: Specific values for extra possible keys in logging formatted string
    """
    method = getattr(logger, level)
    method(msg, extra=extra)


def create_code_description(status_code: int) -> str:
    """Get formatted string with description for server response status code

    Parameters
    ----------
    status_code : Server response status code

    Returns
    -------
    str
        formatted string
    """
    body = f'{status_code} - {responses[status_code]}'
    return body


def create_descriptive_response(status: int) -> Response:
    """Create response with status description body

    Parameters
    ----------
    status : Server response status code

    Returns
    -------
    Response
        aiohttp.Response instance with set body
    """
    return Response(status=status, body=create_code_description(status))


@streamer
async def file_sender(writer, file_path=None):
    """Create asynchronous write stream for chunks in read file

    Parameters
    ----------
    writer : Asynchronous writer
    file_path : Path to file

    """
    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)
