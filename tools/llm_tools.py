"""
Real OpenAI LLM integration layer for JobTailor.
Uses OpenAI's API to generate resume tailoring, company research,
and ATS reasoning text outputs.
"""

import os
from openai import OpenAI
from utils.logger import get_logger
from utils.decorators import retry

logger = get_logger(__name__)


@retry(times=3, delay=2)
def llm_call(
    prompt: str, model: str = None, temperature: float = 0.6, max_tokens: int = 800
) -> dict:
    """
    Call the OpenAI Chat Completion API with a given prompt.

    Args:
        prompt (str): The text prompt for the LLM.
        model (str, optional): Model name (defaults to GPT-4o-mini or env var).
        temperature (float, optional): Creativity level (0.0–1.0).
        max_tokens (int, optional): Response length limit.

    Returns:
        dict: { "response": str, "model": str }
    """
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        logger.warning("OPENAI_API_KEY not set — returning stub response.")
        return {"response": f"[Stub LLM] {prompt[:200]}...", "model": "stub"}

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are JobTailor AI — a helpful assistant that tailors resumes and researches companies.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        result = response.choices[0].message.content.strip()
        logger.info(
            f"LLM ({model}) call succeeded. Tokens used: {response.usage.total_tokens if response.usage else 'N/A'}"
        )
        return {"response": result, "model": model}

    except Exception as e:
        logger.exception("OpenAI API call failed")
        return {"response": f"[Error calling LLM: {e}]", "model": model}
