"""
Custom exceptions for the test application.
"""

class BusinessLogicError(Exception):
    """Custom exception for business logic errors."""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class UserNotFoundError(Exception):
    """Custom exception for user not found errors."""
    pass

class PaymentError(Exception):
    """Custom exception for payment processing errors."""
    pass

class ExternalAPIError(Exception):
    """Custom exception for external API errors."""
    pass
