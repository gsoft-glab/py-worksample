from typing import Dict, Any, Optional

class FunctionCall:
    """
    FunctionCall entity representing a specific call to a function.
    
    This class represents a call to a function with specific parameters
    and the result of the call.
    """
    def __init__(
        self,
        id: str,
        function_id: str,
        parameters: Dict[str, Any],
        result: Optional[Dict[str, Any]] = None,
        status: str = "pending"
    ):
        self.id = id
        self.function_id = function_id
        self.parameters = parameters
        self.result = result
        self.status = status  # pending, completed, failed
    
    def set_result(self, result: Dict[str, Any]) -> None:
        """
        Set the result of the function call and mark it as completed.
        
        Args:
            result: The result of the function call
        """
        self.result = result
        self.status = "completed"
    
    def set_failed(self, error: str) -> None:
        """
        Mark the function call as failed with an error message.
        
        Args:
            error: The error message
        """
        self.result = {"error": error}
        self.status = "failed"
    
    def is_completed(self) -> bool:
        """
        Check if the function call is completed.
        
        Returns:
            True if the function call is completed, False otherwise
        """
        return self.status == "completed"
    
    def is_failed(self) -> bool:
        """
        Check if the function call failed.
        
        Returns:
            True if the function call failed, False otherwise
        """
        return self.status == "failed"
    
    def is_pending(self) -> bool:
        """
        Check if the function call is pending.
        
        Returns:
            True if the function call is pending, False otherwise
        """
        return self.status == "pending"