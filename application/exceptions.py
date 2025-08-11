class ApplicationException(Exception):
    """Base exception for all application exceptions"""
    status_code = 500
    
    def __init__(self, message: str = None):
        self.message = message or "An application error occurred"
        super().__init__(self.message)


class NotFoundException(ApplicationException):
    """Exception raised when a requested resource is not found"""
    status_code = 404
    
    def __init__(self, message: str = None):
        self.message = message or "Resource not found"
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """Exception raised when input validation fails"""
    status_code = 400
    
    def __init__(self, message: str = None):
        self.message = message or "Validation error"
        super().__init__(self.message)