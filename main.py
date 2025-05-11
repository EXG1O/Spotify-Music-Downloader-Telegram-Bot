from bot import bot, dispatcher
from core.tasks import run_tasks

import asyncio


async def main() -> None:
    await run_tasks()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
