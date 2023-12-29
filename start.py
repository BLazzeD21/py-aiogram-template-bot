import asyncio

from bot import main

from logging import RootLogger
from logger import startLogging



if __name__ == '__main__':
  try:
    logger: RootLogger = startLogging()
    asyncio.run(main())
  except KeyboardInterrupt:
    pass