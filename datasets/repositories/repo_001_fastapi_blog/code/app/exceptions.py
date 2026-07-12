class BlogError(Exception):
    """Base class for domain errors that the API layer maps to HTTP responses."""


class PostValidationError(BlogError):
    """Raised when post input fails validation (maps to HTTP 422)."""


class AuthError(BlogError):
    """Raised for authentication failures (maps to HTTP 401)."""


class TokenExpiredError(AuthError):
    """Raised when a token's expiry timestamp has already passed."""
