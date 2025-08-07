# AI Assistant with Function Calling Capabilities

This project implements an AI assistant with function calling capabilities.

## Project Structure

The project is organized into four layers:

1. **API Layer**: Handles HTTP requests/responses, routing, and controllers for the REST API endpoints
2. **Domain Layer**: Contains core business logic, entities, and interfaces
3. **Application Layer**: Orchestrates use cases and transforms data between layers
4. **Infrastructure Layer**: Provides concrete implementations and external service integrations

## Running the Application

1. Install dependencies using uv:
   ```
   uv sync
   ```

2. Run the application using uvicorn:
   ```
   python -m uvicorn main:app --reload
   ```

3. Open your browser and navigate to:
   - API documentation: http://127.0.0.1:8000/docs
   - API root: http://127.0.0.1:8000/

## API Endpoints

### Conversations

- `POST /api/conversations/`: Create a new conversation
- `GET /api/conversations/{conversation_id}`: Get a conversation by ID
- `POST /api/conversations/{conversation_id}/messages`: Add a message to a conversation

### Functions

- `POST /api/functions/`: Register a new function
- `GET /api/functions/`: List all registered functions
- `POST /api/functions/call`: Call a function

## Implementation Notes

- The project uses in-memory storage for simplicity
- The AI assistant functionality is mocked for the purpose of the work sample
- The function calling capability allows the AI assistant to call registered functions