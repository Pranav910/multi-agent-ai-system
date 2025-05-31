from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Production App"
    ENVIRONMENT: str = "production"

settings = Settings()