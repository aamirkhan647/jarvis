import pytest
from unittest.mock import patch
from tools.research_tools import research_company


@patch("tools.research_tools.research_company")
def test_fetch_company_profile(mock_get):
    """
    Simulate fetching company profile info.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><body>OpenAI builds safe AGI</body></html>"
    result = research_company("OpenAI")

    assert isinstance(result, dict)
    assert "openai" in result["description"].lower()
