class FunctionParameter:
    """
    Value object representing a parameter for a function.
    
    This class represents a parameter for a function, including its name,
    type, description, and whether it's required.
    """
    def __init__(
        self,
        name: str,
        type: str,
        description: str,
        required: bool = False
    ):
        self.name = name
        self.type = type
        self.description = description
        self.required = required
    
    def to_dict(self):
        """
        Convert the parameter to a dictionary.
        
        Returns:
            A dictionary representation of the parameter
        """
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FunctionParameter':
        """
        Create a parameter from a dictionary.
        
        Args:
            data: A dictionary containing the parameter data
            
        Returns:
            A new FunctionParameter instance
        """
        return cls(
            name=data.get("name", ""),
            type=data.get("type", "string"),
            description=data.get("description", ""),
            required=data.get("required", False)
        )
    
    def __eq__(self, other):
        """
        Check if two parameters are equal.
        
        Args:
            other: Another parameter to compare with
            
        Returns:
            True if the parameters are equal, False otherwise
        """
        if not isinstance(other, FunctionParameter):
            return False
        
        return (
            self.name == other.name and
            self.type == other.type and
            self.description == other.description and
            self.required == other.required
        )