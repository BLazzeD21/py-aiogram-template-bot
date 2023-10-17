from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu

import handlers

async def main() -> None:  
  configuration: Config = load_config(".env")

  BOT_TOKEN: str = configuration.tg_bot.token
  
  bot: Bot = Bot(token=BOT_TOKEN, parse_mode="html")

  dp: Dispatcher = Dispatcher(configuration=configuration)

  dp.startup.register(set_main_menu)

  dp.include_router(handlers.admin_handlers.router)
  dp.include_router(handlers.user_handlers.router)
  dp.include_router(handlers.other_handlers.router)

  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)