import sys
import asyncio
from pathlib import Path


sys.path.append(str(Path(__file__).parents[1]))

from image_converter.backend.db.settings import ENGINE, BASE
from image_converter.backend.models import Image


async def drop_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(BASE.metadata.drop_all, BASE.metadata.tables.values(), checkfirst=True)


async def main():
    await drop_tables()


if __name__ == '__main__':
    # https://stackoverflow.com/questions/65682221/runtimeerror-exception-ignored-in-function-proactorbasepipetransport
    asyncio.get_event_loop().run_until_complete(main())
