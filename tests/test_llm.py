from unittest.mock import patch, Mock

import pytest

from app.llm import call_llm, ProductAnalysis
from app.exceptions import LLMError


VALID_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": """
                {
                    "summary": "Good value tablet.",
                    "market_position": "Budget-friendly option.",
                    "strengths": [
                        "Affordable price",
                        "Good rating"
                    ],
                    "weaknesses": [
                        "Limited review volume"
                    ],
                    "recommendations": [
                        "Consider improving storage options"
                    ]
                }
                """
            }
        }
    ]
}


@patch("app.llm.requests.post")
@patch("app.llm.os.getenv")
def test_call_llm_success(mock_getenv, mock_post):
    mock_getenv.return_value = "test_api_key"

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = VALID_RESPONSE

    mock_post.return_value = response

    result = call_llm("Analyze this product.")

    assert isinstance(result, ProductAnalysis)
    assert result.summary == "Good value tablet."
    assert result.market_position == "Budget-friendly option."
    assert len(result.strengths) == 2
    assert len(result.weaknesses) == 1
    assert len(result.recommendations) == 1

    mock_post.assert_called_once()


@patch("app.llm.requests.post")
@patch("app.llm.os.getenv")
def test_call_llm_request_failure(mock_getenv, mock_post):
    mock_getenv.return_value = "test_api_key"

    import requests

    mock_post.side_effect = requests.RequestException(
        "Connection failed"
    )

    with pytest.raises(LLMError):
        call_llm("Analyze this product.")


@patch("app.llm.os.getenv")
def test_call_llm_missing_api_key(mock_getenv):
    mock_getenv.return_value = None

    with pytest.raises(LLMError):
        call_llm("Analyze this product.")


@patch("app.llm.requests.post")
@patch("app.llm.os.getenv")
def test_call_llm_invalid_json(mock_getenv, mock_post):
    mock_getenv.return_value = "test_api_key"

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "This is not valid JSON"
                }
            }
        ]
    }

    mock_post.return_value = response

    with pytest.raises(LLMError):
        call_llm("Analyze this product.")


@patch("app.llm.requests.post")
@patch("app.llm.os.getenv")
def test_call_llm_unexpected_response(mock_getenv, mock_post):
    mock_getenv.return_value = "test_api_key"

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "unexpected": "response"
    }

    mock_post.return_value = response

    with pytest.raises(LLMError):
        call_llm("Analyze this product.")