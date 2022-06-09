"""Database setup settings

This file provides database setup initialization and contains:
    Constants:
        * DB_TYPE - database type
        * ASYNC_DIALECT - async dialect for database
        * DB_USER - database user
        * DB_PASSWORD - database password
        * DB_HOST - database host
        * DB_PORT - database port
        * DB_NAME - database name
        * DB_URI_ASYNC - database Async URI
        * DB_URI_SYNC - database sync URI
        * ENGINE - Engine for database
        * ASYNC_SESSION - async session

    Classes:

        * BASE
            ORM base class with bound session
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from image_converter.settings import config


DB_TYPE = config['db']['type']
ASYNC_DIALECT = config['db']['async']
DB_USER = config['db']['user']
DB_PASSWORD = config['db']['password']
DB_HOST = config['db']['host']
DB_PORT = config['db']['port']
DB_NAME = config['db']['name']
DB_URI_ASYNC = f"{DB_TYPE}+{ASYNC_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URI_SYNC = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ENGINE = create_async_engine(DB_URI_ASYNC)
ASYNC_SESSION = sessionmaker(ENGINE, expire_on_commit=False, class_=AsyncSession)
BASE = declarative_base()
BASE.metadata.bind = ENGINE
