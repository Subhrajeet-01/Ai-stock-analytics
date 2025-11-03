from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from . import config

sqlalchemy_database_url = config.SQLALCHEMY_DATABASE_URL
# print("Database URL from connect:", sqlalchemy_database_url)

# db connection setup (example, adjust as needed)
engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()

if __name__ == "__main__":
    # run from project root:
    # python -m backend.src.database.connect
    print("connect module executed as script")