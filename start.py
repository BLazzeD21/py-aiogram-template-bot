import asyncio

from logger import startLogging
from bot import main


if __name__ == '__main__':
  try:
    logger = startLogging()
    asyncio.run(main())
  except KeyboardInterrupt:
    pass