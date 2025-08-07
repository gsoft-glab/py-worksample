from typing import Dict, List, Any

"""
In-memory database for entities.

This module provides a simple in-memory database for entities using a dictionary.
In a real application, this would be replaced with a persistent database.
"""

# Global in-memory database
database: Dict[str, List[Dict[str, Any]]] = {
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
    Get the database dictionary.
    
    Returns:
        The database dictionary
    """
    return database