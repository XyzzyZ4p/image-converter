import sys
import asyncio
from pathlib import Path

import aiofiles

sys.path.append(str(Path(__file__).parents[1]))

from image_converter.backend.db.settings import ASYNC_SESSION
from image_converter.backend.models import User


PROJECT_ROOT = Path(__file__).parents[1]


async def fill_tables():
    async with ASYNC_SESSION() as session:
        async with session.begin():
            user = User()
            session.add(user)
            await session.flush()
            await session.refresh(user)
            async with aiofiles.open(PROJECT_ROOT / 'token', 'w', encoding='utf-8') as f:
                await f.write(f"{user.id}")


async def main():
    await fill_tables()


if __name__ == '__main__':
    # https://stackoverflow.com/questions/65682221/runtimeerror-exception-ignored-in-function-proactorbasepipetransport
    asyncio.get_event_loop().run_until_complete(main())
