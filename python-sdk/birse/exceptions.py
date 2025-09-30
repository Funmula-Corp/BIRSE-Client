class BirseException(Exception):
    """Base exception for BIRSE SDK"""
    pass


class BirseAPIError(BirseException):
    """API related errors"""
    pass


class BirseConnectionError(BirseException):
    """Network connection related errors"""
    pass