from abc import ABC

class Entity(ABC):
    """
    Base class for all domain entities.
    
    This abstract class provides a common interface for all entities,
    ensuring they all have an ID property.
    """
    def __init__(self, id: str):
        self.id = id