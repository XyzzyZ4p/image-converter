import sys
import asyncio
from pathlib import Path

from sqlalchemy_utils import database_exists, create_database

sys.path.append(str(Path(__file__).parents[1]))

from image_converter.backend.db.settings import ENGINE, DB_URI_SYNC
from image_converter.backend.models import *


async def create_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all, BASE.metadata.tables.values(), checkfirst=True)


def create_db():
    exists = database_exists(DB_URI_SYNC)
    if not exists:
        create_database(DB_URI_SYNC)


async def main():
    create_db()
    await create_tables()


if __name__ == '__main__':
    # https://stackoverflow.com/questions/65682221/runtimeerror-exception-ignored-in-function-proactorbasepipetransport
    asyncio.get_event_loop().run_until_complete(main())
