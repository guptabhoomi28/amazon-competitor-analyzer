# Amazon Competitor Analyzer

An AI-powered web application that analyzes an Amazon product, discovers relevant competitors, compares their product information, and generates structured competitive insights using an LLM.

## Features

- Fetch Amazon product information using Oxylabs
- Discover relevant competing products automatically
- Compare product price, rating, reviews, and specifications
- Store product data locally using SQLite
- Cache product data for 24 hours to reduce unnecessary scraping
- Generate AI-powered competitive analysis
- Structured AI responses validated using Pydantic
- Handle scraping, database, and LLM errors with custom exceptions
- Streamlit-based web interface
- Automated tests using pytest
- API calls mocked during testing to avoid unnecessary external requests

## How It Works

```text
                    User
                     │
                     ▼
              Streamlit UI
                     │
                     ▼
             Services Layer
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
       SQLite                Oxylabs
       Database                 │
          │                     ▼
          │             Amazon Product Data
          │                     │
          │                     ▼
          │              Competitor Search
          │                     │
          └──────────┬──────────┘
                     ▼
              OpenRouter LLM
                     │
                     ▼
            Pydantic Validation
                     │
                     ▼
              AI Analysis
                     │
                     ▼
                Streamlit
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web interface |
| SQLite | Local product data storage |
| Oxylabs | Amazon data scraping |
| OpenRouter | LLM API |
| Pydantic | Structured response validation |
| Requests | HTTP API requests |
| python-dotenv | Environment variable management |
| Pytest | Automated testing |

## Project Structure

```text
amazon-competitor-analyzer/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── exceptions.py
│   ├── llm.py
│   ├── main.py
│   ├── oxylabs.py
│   └── services.py
│
├── tests/
│   ├── test_database.py
│   ├── test_llm.py
│   ├── test_oxylabs.py
│   └── test_services.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## Application Flow

1. The user enters an Amazon ASIN.
2. The application checks the SQLite database for cached product data.
3. If the product data is missing or older than 24 hours, fresh data is retrieved using Oxylabs.
4. Amazon search is used to discover potential competitors.
5. The application filters and selects relevant competitors.
6. Detailed competitor information is retrieved.
7. Product and competitor information is sent to the LLM.
8. The LLM generates structured competitive insights.
9. Pydantic validates the AI response.
10. The final analysis is displayed in the Streamlit interface.

## AI Analysis

The application generates structured analysis containing:

- Summary
- Market position
- Strengths
- Weaknesses
- Recommendations

The LLM is instructed to analyze only the information provided by the application and return a predefined JSON structure.

## Data Caching

The application uses SQLite to cache scraped product information.

Product data is considered fresh for **24 hours**.

```text
Request
   │
   ▼
Check SQLite
   │
   ├── Fresh data ──────► Use cached data
   │
   └── Missing/Stale
             │
             ▼
        Scrape Amazon
             │
             ▼
        Update SQLite
```

This reduces unnecessary API calls and improves application performance.

## Error Handling

The application uses custom exceptions for different failure types:

- `ProductNotFoundError` — product cannot be found
- `ScrapingError` — Oxylabs request or scraping failure
- `LLMError` — LLM request or response failure
- `DatabaseError` — database-related failure

This allows different layers of the application to handle errors appropriately.

## Testing

The project uses **pytest** for automated testing.

Run the complete test suite with:

```bash
pytest -v
```

Current test coverage includes:

- Database table creation
- Database insertion and retrieval
- Successful Amazon product scraping
- Successful Amazon search
- Missing Oxylabs credentials
- Oxylabs request failures
- Successful LLM response parsing
- LLM request failures
- Missing OpenRouter API key
- Invalid LLM JSON
- Unexpected LLM responses
- Cached product analysis
- Missing product handling
- Stale competitor refresh

Current test suite:

```text
14 passed
```

External API requests are mocked in the tests, so running the test suite does not require making real Oxylabs or OpenRouter requests.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/guptabhoomi28/amazon-competitor-analyzer.git
cd amazon-competitor-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```text
OXYLABS_USERNAME=your_oxylabs_username
OXYLABS_PASSWORD=your_oxylabs_password
OPENROUTER_API_KEY=your_openrouter_api_key
```

Never commit the `.env` file or expose API keys publicly.

### 6. Run the application

```bash
python -m streamlit run app/main.py
```

The application will open in your browser.

## Example

Enter an Amazon ASIN such as:

```text
B0FGYCJ7NJ
```

The application retrieves the product information, finds competitors, and generates an AI-powered competitive analysis.

## Future Improvements

Potential improvements include:

- More advanced competitor similarity scoring
- Price comparison visualizations
- Historical price tracking
- More detailed product specification comparisons
- Persistent competitor ranking
- Additional Amazon marketplaces
- User authentication
- Deployment to a cloud platform
- More extensive test coverage
- Background scraping jobs

## Author

**Bhoomi Gupta**

Built as a learning and portfolio project focused on Python, APIs, web scraping, databases, LLM integration, testing, and software engineering practices.