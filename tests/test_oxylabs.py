from unittest.mock import patch, Mock

import pytest

from app.oxylabs import scrape_product, search_amazon
from app.exceptions import ScrapingError


def mock_product_response():
    return {
        "results": [
            {
                "content": {
                    "asin": "TEST123",
                    "title": "Test Tablet",
                    "brand": "Test Brand",
                    "price": 199.99,
                    "currency": "USD",
                    "rating": 4.5,
                    "reviews_count": 100,
                    "stock": "In Stock",
                    "url": "https://amazon.com/dp/TEST123",
                    "images": [],
                    "configuration": "10 inch display",
                    "screen_size": "10 inches",
                    "display_resolution_maximum": "1920 x 1200",
                    "display_refresh_rate_in_hertz": "60",
                    "processor_description": "Test Processor",
                    "battery_average_life": "10 hours",
                    "operating_system": "Android",
                    "included_components": "Tablet, Cable",
                }
            }
        ]
    }


def mock_search_response():
    return {
        "results": [
            {
                "content": {
                    "results": {
                        "organic": [
                            {
                                "asin": "TEST123",
                                "title": "Test Tablet",
                                "price": 199.99,
                                "currency": "USD",
                                "rating": 4.5,
                                "reviews_count": 100,
                                "url": "https://amazon.com/dp/TEST123",
                                "url_image": "https://example.com/image.jpg",
                                "is_sponsored": False,
                            }
                        ]
                    }
                }
            }
        ]
    }


@patch("app.oxylabs.requests.post")
@patch("app.oxylabs.os.getenv")
def test_scrape_product_success(mock_getenv, mock_post):
    mock_getenv.side_effect = lambda key: {
        "OXYLABS_USERNAME": "test_user",
        "OXYLABS_PASSWORD": "test_password",
    }.get(key)

    response = Mock()
    response.json.return_value = mock_product_response()
    response.raise_for_status.return_value = None

    mock_post.return_value = response

    result = scrape_product("TEST123")

    assert result["asin"] == "TEST123"
    assert result["title"] == "Test Tablet"
    assert result["brand"] == "Test Brand"
    assert result["price"] == 199.99

    mock_post.assert_called_once()


@patch("app.oxylabs.requests.post")
@patch("app.oxylabs.os.getenv")
def test_search_amazon_success(mock_getenv, mock_post):
    mock_getenv.side_effect = lambda key: {
        "OXYLABS_USERNAME": "test_user",
        "OXYLABS_PASSWORD": "test_password",
    }.get(key)

    response = Mock()
    response.json.return_value = mock_search_response()
    response.raise_for_status.return_value = None

    mock_post.return_value = response

    result = search_amazon("test tablet")

    assert len(result) == 1
    assert result[0]["asin"] == "TEST123"
    assert result[0]["title"] == "Test Tablet"

    mock_post.assert_called_once()


@patch("app.oxylabs.os.getenv")
def test_scrape_product_missing_credentials(mock_getenv):
    mock_getenv.return_value = None

    with pytest.raises(ScrapingError):
        scrape_product("TEST123")


@patch("app.oxylabs.requests.post")
@patch("app.oxylabs.os.getenv")
def test_scrape_product_request_failure(mock_getenv, mock_post):
    mock_getenv.side_effect = lambda key: {
        "OXYLABS_USERNAME": "test_user",
        "OXYLABS_PASSWORD": "test_password",
    }.get(key)

    import requests

    mock_post.side_effect = requests.RequestException("Connection failed")

    with pytest.raises(ScrapingError):
        scrape_product("TEST123")