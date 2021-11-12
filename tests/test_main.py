import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from fastapi_confz_demo.main import app, get_session, User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


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
