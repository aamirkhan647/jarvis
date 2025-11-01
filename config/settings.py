import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        # Load from argument if provided, otherwise load from environment
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.KEYWORD_THRESHOLD: float = float(os.getenv("KEYWORD_THRESHOLD", 0.5))


# Create the singleton instance for production/runtime use
settings = Settings()
