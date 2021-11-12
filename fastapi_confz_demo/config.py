from pathlib import Path
from typing import List, Union, Optional

from confz import ConfZ, ConfZDataSource
from pydantic import AnyUrl, SecretStr


class AppConfig(ConfZ):
    title: str
    version: str
    cors_origins: List[AnyUrl]

    CONFIG_SOURCES = ConfZDataSource(data={
        "title": "my-title",
        "version": "0.1.0",
        "cors_origins": [
            "http://localhost",
            "http://localhost:8080"
        ]
    })


class SQLiteDB(ConfZ):
    path: Optional[Path]


class PostgreSQL(ConfZ):
    user: str
    password: SecretStr
    host: str
    database: str


DBTypes = Union[SQLiteDB, PostgreSQL]


class DBConfig(ConfZ):
    echo: bool
    db: DBTypes

    CONFIG_SOURCES = ConfZDataSource(data={
        "echo": True,
        # "db": {"path": None},
        "db": {"path": "database.db"},
        # "db": {
        #     "user": "my-user",
        #     "password": "my-password",
        #     "host": "localhost",
        #     "database": "my-database",
        # }
    })
