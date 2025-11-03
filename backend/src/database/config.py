import os
import csv
from dotenv import load_dotenv

load_dotenv("/home/user/Desktop/LLM_Projects/Ai-stock-analytics/backend/src/database/.env")
DATABASE_USERNAME = os.getenv("database_username")
DATABASE_PASSWORD = os.getenv("database_password")
DATABASE_HOSTNAME = os.getenv("database_hostname")
DATABASE_PORT = os.getenv("database_port")
DATABASE_NAME = os.getenv("database_name")
SQLALCHEMY_DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}'
# print("Database URL from config:", SQLALCHEMY_DATABASE_URL)

if __name__ == "__main__":
    # run from project root:
    # python -m backend.src.database.connect
    print("connect module executed as script")