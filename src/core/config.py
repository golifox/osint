import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
base_dir = Path(__file__).resolve().parent.parent.parent


@dataclass
class Database:
    file: str
    path: Path


@dataclass
class Logging:
    level: str
    file: str
    format: str


@dataclass
class Config:
    database: Database
    logging: Logging


log_config = Logging(
    level="INFO",
    file="info.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)

db_file = os.getenv("DB_FILE")
db_config = Database(file=db_file, path=base_dir / db_file)

config = Config(database=db_config, logging=log_config)
