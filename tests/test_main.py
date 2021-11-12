import pytest
from confz import ConfZDataSource
from fastapi.testclient import TestClient
from sqlmodel import Session

from fastapi_confz_demo.app import app, User, on_startup
from fastapi_confz_demo.config import DBConfig
from fastapi_confz_demo.db import get_engine


# TODO: refactor fixtures (e.g. global db fixture, session fixture and client fixture?)
# TODO: also use auto-fixture so never accidentally access prod db

@pytest.fixture(name="session")
def session_fixture():
    new_sources = ConfZDataSource(data={
        "echo": False,  # TODO
        "db": {"path": None}
    })
    with DBConfig.change_config_sources(new_sources):
        on_startup()
        engine = get_engine()
        with Session(engine) as session:
            yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    client = TestClient(app)
    yield client


def test_create_user(client: TestClient):
    response = client.post(
        "/user/", json={"name": "MyName"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "MyName"
    assert data["id"] is not None


def test_create_user_incomplete(client: TestClient):
    response = client.post(
        "/user/", json={"not-needed": "empty"}
    )
    assert response.status_code == 422


def test_create_user_invalid(client: TestClient):
    response = client.post(
        "/user/", json={"name": {"something": "useless"}}
    )
    assert response.status_code == 422


def test_read_users(session: Session, client: TestClient):
    user_1 = User(name="User1")
    user_2 = User(name="User2")
    session.add(user_1)
    session.add(user_2)
    session.commit()

    response = client.get("/user/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == user_1.name
    assert data[0]["id"] == user_1.id
    assert data[1]["name"] == user_2.name
    assert data[1]["id"] == user_2.id
