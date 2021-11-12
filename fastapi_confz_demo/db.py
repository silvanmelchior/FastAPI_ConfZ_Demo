from confz import depends_on
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from fastapi_confz_demo.config import DBTypes, SQLiteDB, PostgreSQL, DBConfig


def get_db_args(db: DBTypes):
    if isinstance(db, SQLiteDB):
        connect_args = {"check_same_thread": False}
        if db.path is None:
            url = "sqlite://"
            args = {"connect_args": connect_args, "poolclass": StaticPool}
        else:
            url = f"sqlite:///{db.path}"
            args = {"connect_args": connect_args}
    elif isinstance(db, PostgreSQL):
        url = f"postgresql://{db.user}:{db.password.get_secret_value()}@{db.host}/{db.database}"
        args = {}
    else:
        raise ValueError(f"Invalid DB type '{type(db)}'.")

    return url, args


@depends_on(DBConfig)
def get_engine():
    url, args = get_db_args(DBConfig().db)
    engine = create_engine(url, echo=DBConfig().echo, **args)
    return engine


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    with Session(get_engine()) as session:
        yield session
