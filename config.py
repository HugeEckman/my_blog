from pathlib import Path

from sqlalchemy import create_engine

BASE_DIR = Path(__file__).parent
db_file_path = BASE_DIR / "blog.sqlite3"

SQLITE_URL = f"sqlite:///{db_file_path}"
POSTGRESQL_URL = 'postgresql+psycopg2://otus:otus12345@localhost:5433/my_blog'

engine = create_engine(
    url=SQLITE_URL,
    echo=True,
)

engine_postgres = create_engine(
    url=POSTGRESQL_URL,
    echo=True,
)
