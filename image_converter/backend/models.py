"""database ORM Models

This file provides models for models dor database and contains the following
classes:

    * Image
    * User
"""

import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from .db.settings import BASE


class Image(BASE):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True),
                name='image_id',
                primary_key=True,
                default=uuid.uuid4)


class User(BASE):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),
                name='user_id',
                primary_key=True,
                default=uuid.uuid4)
