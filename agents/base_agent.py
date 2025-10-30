from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from config.settings import settings


class BaseAgent:
    """Base class for all agents to handle LLM initialization."""

    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in settings.")

        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY, model=model_name, temperature=0.2
        )

    def get_parser(self, pydantic_schema):
        """Returns a Pydantic output parser instance for structured output."""
        return PydanticOutputParser(pydantic_object=pydantic_schema)
