from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

user = os.getenv("TEST_POSTGRES_USER")
password = os.getenv("TEST_POSTGRES_PASSWORD")
host = os.getenv("TEST_POSTGRES_HOST")
port = os.getenv("TEST_POSTGRES_PORT")
db = os.getenv("TEST_POSTGRES_DB")

URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(
    URL, pool_size=50, echo=False
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()
