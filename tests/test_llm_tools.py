import os
import pytest
from unittest.mock import patch, MagicMock

from agents.tools.llm_tools import llm_call


def test_llm_call_stub_mode(monkeypatch):
    """
    Test stub mode when OPENAI_API_KEY is not set.
    """
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = llm_call("Test prompt for stub.")
    assert "Stub LLM" in result["response"]
    assert "model" in result


@patch("agents.tools.llm_tools.OpenAI")
def test_llm_call_success(mock_openai, monkeypatch):
    """
    Test successful OpenAI response using mock.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    # Create fake client + response
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="This is an AI response"))
    ]
    mock_response.usage = MagicMock(total_tokens=123)
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    result = llm_call("Write a summary about Python.")
    assert "AI response" in result["response"]
    assert result["model"] == "GPT-4o-mini"


@patch("agents.tools.llm_tools.OpenAI")
def test_llm_call_failure(mock_openai, monkeypatch):
    """
    Test API failure handling.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Simulated API failure")
    mock_openai.return_value = mock_client

    result = llm_call("Trigger failure.")
    assert "Error calling LLM" in result["response"]
