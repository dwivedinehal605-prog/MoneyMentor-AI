from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# DATABASE_URL tells SQLAlchemy which database to connect to and how to connect.
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)

# think of Engine is as database manager it knows where DB is, how to connect, how to send SQL queries, how to receive results.
# create_engine() Creates the database engine.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session is a temporary conversation with the database. Python wouldn't know how to execute operations.
# Session is used for insert, update, delete, read.
# SessionLocal is a factory that creates new database sessions for each request.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
# Dependency
def get_db(): # get_db() Provides one session per request and closes it automatically
    db = SessionLocal()
    try:
        yield db # yield, Supplies the session and resumes later to clean it up
    finally:
        db.close()