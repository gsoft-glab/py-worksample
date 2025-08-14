# AI Assistant with Function Calling

A Python-based AI assistant that processes natural language requests and executes appropriate functions.

## Features

- **Natural Language Processing**: Understands user requests and identifies required functions
- **Function Calling**: Automatically extracts parameters and executes functions
- **REST API**: FastAPI backend with conversation and function endpoints
- **Chat Interface**: Gradio UI for interactive conversations
- **Supported Functions**: Weather information, time queries, and basic calculations

## Project Structure

The project is organized into four layers:

1. **API Layer**: Handles HTTP requests/responses and routing
2. **Application Layer**: Orchestrates use cases and transforms data
3. **Domain Layer**: Contains core business logic and entities
4. **Infrastructure Layer**: Provides implementations and integrations

## Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation & Setup

1. Install dependencies:
   ```
   uv sync
   ```

2. Start the backend API:
   ```
   uv run python -m uvicorn main:app --reload
   ```
   Access API docs at http://127.0.0.1:8000/docs

3. In a new terminal, start the Gradio UI:
   ```
   uv run python gradio_ui.py
   ```
   Access the chat interface at http://127.0.0.1:7860

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/conversations/` | POST | Create a new conversation |
| `/api/conversations/{id}` | GET | Get conversation by ID |
| `/api/conversations/{id}/messages` | GET | Get conversation messages |
| `/api/conversations/{id}/messages` | POST | Add message to conversation |
| `/api/functions/` | GET | List available functions |
| `/api/functions/call` | POST | Call a function |

## Using the Chat Interface

The Gradio UI provides a simple chat interface. Try these example prompts:
- "What's the weather in New York?"
- "What time is it now?"
- "Calculate 15 × 7"

## Implementation Notes

- Uses in-memory storage for simplicity
- AI service is mocked for demonstration

## Testing

Run the test suite:
```
python -m pytest tests/
```

## Planned Features

1. Implement API key authorization for secure access to the API endpoints
2. Add a `generate_random_number` function that generates a random number within a specified range
3. Create an endpoint to generate summaries of conversations