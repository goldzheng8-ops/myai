import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent

for env_path in (BACKEND_DIR / ".env", PROJECT_ROOT / ".env"):
    if env_path.exists():
        load_dotenv(env_path, override=False)


class Settings(BaseModel):
    app_name: str = "AI SPACE"
    version: str = "0.1.0"
    database_url: str | None = os.getenv("DATABASE_URL")


settings = Settings()