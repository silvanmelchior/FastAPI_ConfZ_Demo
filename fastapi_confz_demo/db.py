from sqlmodel import SQLModel, Session, create_engine


def get_engine():
    engine = create_engine("sqlite:///dev_db.db", echo=True, connect_args={"check_same_thread": False})
    return engine


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    with Session(get_engine()) as session:
        yield session
