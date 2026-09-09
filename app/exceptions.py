class ProductNotFoundError(Exception):
    """Raised when an Amazon product cannot be found."""
    pass


class ScrapingError(Exception):
    """Raised when an Oxylabs request fails."""
    pass


class LLMError(Exception):
    """Raised when the LLM request or response fails."""
    pass


class DatabaseError(Exception):
    """Raised when a database operation fails."""
    pass