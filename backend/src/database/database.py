from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_HOST = os.getenv("PGHOST", "localhost")
POSTGRES_PORT = os.getenv("PGPORT", "5432")
POSTGRES_USER = os.getenv("PGUSER", "postgres")
POSTGRES_PASSWORD = os.getenv("PGPASSWORD", "postgres")
POSTGRES_DB = os.getenv("PGDATABASE", "postgres")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()