from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


user = "postgres"
password = ""
host = "localhost"
db = "blog"
port = 5432

URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(
    URL, pool_size=50, echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()