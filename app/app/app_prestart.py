import asyncio
import logging

from sqlalchemy import text
from tenacity import retry
from tenacity.after import after_log
from tenacity.before import before_log
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from app import log
from app.db.session import AsyncDbSession

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


log.info("App prestart")


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(log, logging.INFO),
    after=after_log(log, logging.WARN),
)
async def init() -> None:
    db = AsyncDbSession()

    try:
        await db.execute(text("SELECT 1"))
        return

    except Exception as e:
        log.error(e)
        raise e

    finally:
        await db.close()


async def main() -> int:
    log.info("Testing DB connection")
    await init()
    log.info("DB connection successful")
    return 0


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
