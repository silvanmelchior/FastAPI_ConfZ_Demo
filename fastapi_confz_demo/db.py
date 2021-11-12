from confz import depends_on
from sqlmodel import SQLModel, Session, create_engine

from fastapi_confz_demo.config import DBTypes, SQLiteDB, PostgreSQL, DBConfig


def get_db_url(db: DBTypes):
    if isinstance(db, SQLiteDB):
        if db.path is None:
            return "sqlite://"
        return f"sqlite:///{db.path}"
    if isinstance(db, PostgreSQL):
        return f"postgresql://{db.user}:{db.password.get_secret_value()}@{db.host}/{db.database}"

    raise ValueError(f"Invalid DB type '{type(db)}'.")


@depends_on(DBConfig)
def get_engine():
    connect_args = {"check_same_thread": False}
    url = get_db_url(DBConfig().db)
    engine = create_engine(url, echo=DBConfig().echo, connect_args=connect_args)
    return engine


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    with Session(get_engine()) as session:
        yield session
