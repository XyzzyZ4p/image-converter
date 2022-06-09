"""Decorators for views

This file provides decorators for project views and contains the following
functions:

    * request_log(method): - returns wrapped function with log features
    * auth(method) - returns wrapped function with authorization features
"""

import logging
import functools
from http import HTTPStatus

from sqlalchemy.exc import DBAPIError
from aiohttp.web import Response

from image_converter.settings import config
from image_converter.backend.models import User
from image_converter.backend.views.helpers import create_code_description


def request_log(method):
    """Provided decorated method with log features

    Parameters
    ----------
    method : Callable
        wrapping method

    Returns
    -------
    Callable
        wrapped function
    """
    log = logging.getLogger(config['project']['name'])

    @functools.wraps(method)
    async def inner(ref, request):
        extra = {'route': request.url, 'functionName': method.__name__}
        log.info(f'Receive request', extra=extra)
        result = await method(ref, request)
        status = result.status
        log.info(f'Response status: {status}', extra=extra)
        return result
    return inner


def auth(method):
    """Provided decorated method with auth features

    Parameters
    ----------
    method : Callable
        wrapping method

    Returns
    -------
    Callable
        wrapped function
    """
    log = logging.getLogger(config['project']['name'])

    @functools.wraps(method)
    async def inner(ref, request):
        extra = {'route': request.url, 'functionName': method.__name__}
        _token = request.headers['Authorization']
        log.info(f'Auth Request {_token}', extra=extra)

        token = _token.split(' ')
        if len(token) == 2:
            token = token[1]
            session = request.app['db']

            try:
                async with session.begin():
                    await session.get(User, token)
            except DBAPIError:
                status = HTTPStatus.UNAUTHORIZED
                log.info(f'User with token {_token} not found',
                         extra={'route': request.url, 'functionName': method.__name__})
                return Response(status=status, body=create_code_description(status))
            else:
                log.info(f'User {_token} Authorized',
                         extra={'route': request.url, 'functionName': method.__name__})
                return await method(ref, request)
        else:
            status = HTTPStatus.BAD_REQUEST
            log.info(f'Bad token data {_token} provided',
                     extra={'route': request.url, 'functionName': method.__name__})
            return Response(status=status, body=create_code_description(status))

    return inner
