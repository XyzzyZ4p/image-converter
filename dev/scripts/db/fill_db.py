import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parents[3]))

from image_converter.backend.db.settings import ASYNC_SESSION
from image_converter.backend.models import Image


async def fill_tables():
    async with ASYNC_SESSION() as session:
        async with session.begin():
            for _ in range(10):
                image = Image()
                session.add(image)


async def main():
    await fill_tables()


if __name__ == '__main__':
    # https://stackoverflow.com/questions/65682221/runtimeerror-exception-ignored-in-function-proactorbasepipetransport
    asyncio.get_event_loop().run_until_complete(main())
