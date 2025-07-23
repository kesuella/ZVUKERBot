from dataclasses import dataclass
from typing import Any
from pydantic import BaseSettings

@dataclass
class BotConfig:
    token: str

class Settings(BaseSettings):
    bot: BotConfig
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings()
