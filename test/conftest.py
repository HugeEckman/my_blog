from sqlalchemy.orm import Session
from pytest import fixture
import config


@fixture()
def db_session():
    with Session(config.engine) as session:
        yield session

    