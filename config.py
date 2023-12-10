from pathlib import Path

from sqlalchemy import create_engine

BASE_DIR = Path(__file__).parent
db_file_path = BASE_DIR / "blog.sqlite3"

DB_URL = f"sqlite:///{db_file_path}"
DB_ECHO = True

engine = create_engine(
    url=DB_URL,
    echo=DB_ECHO,
)

engine_postgres = create_engine(
    url='postgresql+psycopg2://otus:otus12345@localhost:5434/my_blog',
    echo=True,
)
