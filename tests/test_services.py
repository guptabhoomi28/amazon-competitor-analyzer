from unittest.mock import patch

from app.services import analyze_product


PRODUCT = {
    "asin": "TEST123",
    "title": "Test Tablet",
    "brand": "Test Brand",
    "price": 199.99,
    "currency": "USD",
    "rating": 4.5,
    "reviews_count": 100,
    "stock": "In Stock",
    "url": "https://example.com",
    "images": [],
    "configuration": "10 inch display",
    "screen_size": "10 inches",
    "display_resolution": "1920 x 1200",
    "refresh_rate": "60",
    "processor": "Test Processor",
    "battery_life": "10 hours",
    "operating_system": "Android",
    "included_components": "Tablet, Cable",
    "last_scraped_at": "2026-09-09T10:00:00+00:00",
}


COMPETITOR = {
    "asin": "COMP456",
    "parent_asin": "TEST123",
    "title": "Competitor Tablet",
    "brand": "Competitor Brand",
    "price": 219.99,
    "currency": "USD",
    "rating": 4.4,
    "reviews_count": 80,
    "stock": "In Stock",
    "url": "https://example.com/competitor",
    "images": [],
    "configuration": "10 inch display",
    "screen_size": "10 inches",
    "display_resolution": "1920 x 1200",
    "refresh_rate": "60",
    "processor": "Competitor Processor",
    "battery_life": "9 hours",
    "operating_system": "Android",
    "included_components": "Tablet, Cable",
    "last_scraped_at": "2026-09-09T10:00:00+00:00",
}


ANALYSIS = {
    "summary": "Good value tablet.",
    "market_position": "Budget-friendly option.",
    "strengths": ["Affordable price"],
    "weaknesses": ["Limited reviews"],
    "recommendations": ["Increase storage options"],
}


@patch("app.services.call_llm")
@patch("app.services.scrape_competitors")
@patch("app.services.find_competitors")
@patch("app.services.get_competitors")
@patch("app.services.get_product")
def test_analyze_product_uses_cached_data(
    mock_get_product,
    mock_get_competitors,
    mock_find_competitors,
    mock_scrape_competitors,
    mock_call_llm,
):
    mock_get_product.return_value = PRODUCT
    mock_get_competitors.return_value = [COMPETITOR]
    mock_call_llm.return_value = ANALYSIS

    result = analyze_product("TEST123")

    assert result["product"] == PRODUCT
    assert result["competitors"] == [COMPETITOR]
    assert result["analysis"] == ANALYSIS

    mock_find_competitors.assert_not_called()
    mock_scrape_competitors.assert_not_called()
    mock_call_llm.assert_called_once()


@patch("app.services.call_llm")
@patch("app.services.scrape_competitors")
@patch("app.services.find_competitors")
@patch("app.services.insert_product")
@patch("app.services.scrape_product")
@patch("app.services.get_competitors")
@patch("app.services.get_product")
def test_analyze_product_scrapes_when_product_missing(
    mock_get_product,
    mock_get_competitors,
    mock_scrape_product,
    mock_insert_product,
    mock_find_competitors,
    mock_scrape_competitors,
    mock_call_llm,
):
    mock_get_product.return_value = None
    mock_scrape_product.return_value = PRODUCT
    mock_get_competitors.return_value = [COMPETITOR]
    mock_call_llm.return_value = ANALYSIS

    result = analyze_product("TEST123")

    mock_scrape_product.assert_called_once_with("TEST123")
    mock_insert_product.assert_called_once_with(PRODUCT)

    assert result["product"] == PRODUCT
    assert result["analysis"] == ANALYSIS


@patch("app.services.call_llm")
@patch("app.services.scrape_competitors")
@patch("app.services.find_competitors")
@patch("app.services.get_competitors")
@patch("app.services.get_product")
def test_analyze_product_refreshes_stale_competitors(
    mock_get_product,
    mock_get_competitors,
    mock_find_competitors,
    mock_scrape_competitors,
    mock_call_llm,
):
    stale_competitor = COMPETITOR.copy()
    stale_competitor["last_scraped_at"] = "2020-01-01T00:00:00+00:00"

    mock_get_product.return_value = PRODUCT
    mock_get_competitors.return_value = [stale_competitor]
    mock_find_competitors.return_value = [
        {
            "asin": "COMP456",
            "title": "Competitor Tablet",
        }
    ]
    mock_scrape_competitors.return_value = [COMPETITOR]
    mock_call_llm.return_value = ANALYSIS

    result = analyze_product("TEST123")

    mock_find_competitors.assert_called_once()
    mock_scrape_competitors.assert_called_once()

    assert result["competitors"] == [COMPETITOR]
    assert result["analysis"] == ANALYSIS