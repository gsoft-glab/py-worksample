from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Result(Generic[T]):
    """
    A class to represent the result of an operation.
    """
    def __init__(self, success: bool, value: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.value = value
        self.error = error
    
    @classmethod
    def success(cls, value: T) -> 'Result[T]':
        return cls(True, value, None)
    
    @classmethod
    def failure(cls, error: str) -> 'Result[T]':
        return cls(False, None, error)
    
    def is_success(self) -> bool:
        return self.success
    
    def is_failure(self) -> bool:
        return not self.success
    
    def get_value(self) -> T:
        if self.is_failure():
            raise ValueError(f"Cannot get value from a failed result: {self.error}")
        return self.value
    
    def get_error(self) -> str:
        if self.is_success():
            raise ValueError("Cannot get error from a successful result")
        return self.error