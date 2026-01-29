"""
Middleware module - Middlewares de la aplicación SGG-API
"""

from app.middleware.authentication import AuthenticationMiddleware
from app.middleware.gym_context import GymContextMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware

__all__ = [
    "AuthenticationMiddleware",
    "GymContextMiddleware",
    "LoggingMiddleware",
    "ErrorHandlerMiddleware",
    "RateLimiterMiddleware",
]