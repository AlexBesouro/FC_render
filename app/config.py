from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv(".env.py")

database_hostname = os.getenv("DATABASE_HOSTNAME")
database_password = os.getenv("DATABASE_PASSWORD")
database_username = os.getenv("DATABASE_USERNAME")
database_name = os.getenv("DATABASE_NAME")
database_port = os.getenv("DATABASE_PORT")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_username: str
    database_name: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # class Config:
    #     env_file = ".env.py"

settings = Settings()
