from typing import List

from confz import validate_all_configs
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from fastapi_confz_demo.db import create_db_and_tables, get_session
from fastapi_confz_demo.models import User, UserRead, UserCreate

app = FastAPI(title="My API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "https://my-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    validate_all_configs(include_listeners=True)
    create_db_and_tables()


@app.post("/user/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/user/", response_model=List[UserRead])
def read_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
