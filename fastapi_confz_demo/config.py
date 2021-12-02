from pathlib import Path
from typing import List, Union, Optional, Literal

from confz import ConfZ, ConfZFileSource, ConfZEnvSource
from pydantic import AnyUrl, SecretStr

CONFIG_DIR = Path(__file__).parent.parent.resolve() / "config"


class AppConfig(ConfZ):
    title: str
    version: str
    cors_origins: List[AnyUrl]

    CONFIG_SOURCES = ConfZFileSource(file=CONFIG_DIR / "api.yml")


class SQLiteDB(ConfZ):
    type: Literal["sqlite"]
    path: Optional[Path]  # None if in-memory


class PostgreSQL(ConfZ):
    type: Literal["postgresql"]
    user: str
    password: SecretStr
    host: str
    database: str


DBTypes = Union[SQLiteDB, PostgreSQL]


class DBConfig(ConfZ):
    echo: bool
    db: DBTypes

    CONFIG_SOURCES = [
        ConfZFileSource(
            folder=CONFIG_DIR,
            file_from_env="DB_ENV"
        ),
        ConfZEnvSource(allow=[
            "db.user",
            "db.password"
        ])
    ]
