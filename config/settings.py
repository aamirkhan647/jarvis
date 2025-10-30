import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    KEYWORD_THRESHOLD: float = float(os.getenv("KEYWORD_THRESHOLD", 0.5))


settings = Settings()
