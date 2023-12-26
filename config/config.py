from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]


@dataclass
class RedisConfig:
    host: str
    port: str
    password: str
    db: str


@dataclass
class Config:
    bot: TelegramBot
    redis: RedisConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=TelegramBot(
            token=env("BOT_TOKEN"),
            admin_ids=env.list("ADMIN_IDS", subcast=int),
        ),
        redis=RedisConfig(
            host=env("REDIS_HOST"),
            port=env("REDIS_PORT"),
            password=env("REDIS_PASSWORD"),
            db=env("REDIS_DB"),
        ),
    )
