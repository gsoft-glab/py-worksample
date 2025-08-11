from typing import Dict, List
from domain.entities.entity import Entity

"""
In-memory database for entities.

This module provides a simple in-memory database for entities.
"""

# Global in-memory database storing domain objects
database: Dict[str, List[Entity]] = {
    "messages": [],
    "conversations": [],
    "functions": [],
    "function_calls": []
}

def clear_database():
    """
    Clear all data from the database.
    
    This is useful for testing.
    """
    database["messages"] = []
    database["conversations"] = []
    database["functions"] = []
    database["function_calls"] = []

def get_database():
    """
    Get the database.
    
    Returns:
        The database containing domain object collections
    """
    return database