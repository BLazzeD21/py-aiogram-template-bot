from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    redis_host: str
    redis_port: str
    redis_password: str
    redis_db: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            admin_ids=env.list("ADMIN_IDS", subcast=int),
        ),
        db=DatabaseConfig(
            redis_host=env("REDIS_HOST"),
            redis_port=env("REDIS_PORT"),
            redis_password=env("REDIS_PASSWORD"),
            redis_db=env("REDIS_DB"),
        ),
    )
