import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sulabhai.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")

    class Config:
        env_file = ".env"

settings = Settings()
os.makedirs(settings.upload_dir, exist_ok=True)
