import sys
import os
# from os.path import abspath, dirname

from os.path import abspath, dirname

from sqlalchemy.orm import Session

from pytest import fixture

# from models.model import User, Post, Tag

# from config import engine

# from ..config import engine

# import ../config

import config

print(config.engine)

# or
# from config import engine
# print(engine)


# @fixture()
# def db_session():
#     with Session(config.engine) as session:
#         yield session
#
#     session = Session(engine)
#     yield session
#     session.close()
    