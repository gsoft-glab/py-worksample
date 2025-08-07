from typing import TypeVar, Generic, Optional, Any

T = TypeVar('T')

class Result(Generic[T]):
    """
    A class to represent the result of an operation.
    """
    def __init__(self, success: bool, value: Optional[T] = None, error: Optional[str] = None):
        """
        Initialize a result.
        
        Args:
            success: Whether the operation was successful
            value: The value returned by the operation (if successful)
            error: The error message (if unsuccessful)
        """
        self.success = success
        self.value = value
        self.error = error
    
    @classmethod
    def success(cls, value: T) -> 'Result[T]':
        """
        Create a successful result.
        
        Args:
            value: The value returned by the operation
            
        Returns:
            A successful result
        """
        return cls(True, value, None)
    
    @classmethod
    def failure(cls, error: str) -> 'Result[T]':
        """
        Create a failed result.
        
        Args:
            error: The error message
            
        Returns:
            A failed result
        """
        return cls(False, None, error)
    
    def is_success(self) -> bool:
        """
        Check if the result is successful.
        
        Returns:
            True if the result is successful, False otherwise
        """
        return self.success
    
    def is_failure(self) -> bool:
        """
        Check if the result is a failure.
        
        Returns:
            True if the result is a failure, False otherwise
        """
        return not self.success
    
    def get_value(self) -> T:
        """
        Get the value of the result.
        
        Returns:
            The value of the result
            
        Raises:
            ValueError: If the result is a failure
        """
        if self.is_failure():
            raise ValueError(f"Cannot get value from a failed result: {self.error}")
        return self.value
    
    def get_error(self) -> str:
        """
        Get the error message of the result.
        
        Returns:
            The error message
            
        Raises:
            ValueError: If the result is successful
        """
        if self.is_success():
            raise ValueError("Cannot get error from a successful result")
        return self.error