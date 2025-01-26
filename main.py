from bot import bot, dispatcher
from core.tasks import run_tasks
from database import create_database_tables

import asyncio


async def main() -> None:
    await create_database_tables()
    await run_tasks()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
