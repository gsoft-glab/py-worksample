# AI Assistant with Function Calling Capabilities

This project implements an AI assistant that can understand natural language requests and execute functions based on those requests.

## Project Structure

The project is organized into four layers:

1. **API Layer**: Handles HTTP requests/responses, routing, and controllers for the REST API endpoints
2. **Domain Layer**: Contains core business logic, entities, and interfaces
3. **Application Layer**: Orchestrates use cases and transforms data between layers
4. **Infrastructure Layer**: Provides concrete implementations and external service integrations

## Running the Application

### Backend API

1. Install dependencies using uv:
   ```
   uv sync
   ```

2. Run the application using uvicorn (or launch with vscode):
   ```
   python -m uvicorn main:app --reload
   ```

3. Open your browser and navigate to:
   - API documentation: http://127.0.0.1:8000/docs
   - API root: http://127.0.0.1:8000/

### Gradio UI

The project includes a Gradio-based chat interface for interacting with the AI assistant:

1. Make sure the backend API is running (see above)

2. Start the Gradio UI:
   ```
   python gradio_ui.py
   ```

3. Open your browser and navigate to the URL displayed in the terminal (typically http://127.0.0.1:7860)

## API Endpoints

### Conversations

- `POST /api/conversations/`: Create a new conversation
- `GET /api/conversations/{conversation_id}`: Get a conversation by ID
- `GET /api/conversations/{conversation_id}/messages`: Get all messages in a conversation
- `POST /api/conversations/{conversation_id}/messages`: Add a message to a conversation

### Functions

- `GET /api/functions/`: List all registered functions
- `POST /api/functions/call`: Call a function

## Gradio UI

The Gradio UI provides a user-friendly chat interface to interact with the AI assistant.

### Example Prompts

Try these example prompts to see the function calling capabilities in action:

1. **Weather Function**:
   - "What's the weather like in New York?"
   - "Tell me the forecast for San Francisco"
   - "Is it sunny in Miami?"

2. **Time Function**:
   - "What time is it now?"
   - "Tell me the current time in UTC"
   - "What's the time in London?"

3. **Calculator Function**:
   - "Can you add 5 + 3 for me?"
   - "What's 10 multiplied by 7?"
   - "Calculate 100 divided by 4"

## Implementation Notes

- **In-Memory Storage**: The project uses in-memory storage for simplicity
- **Mocked AI Service**: The AI assistant functionality is mocked for demonstration purposes
- **Function Calling**: The system can detect when a user's message implies a function call, extract relevant parameters, and execute the function
- **Supported Functions**: The system includes three mock functions:
  - `get_weather`: Returns weather information for a location
  - `get_time`: Returns the current time for a timezone
  - `calculate`: Performs basic arithmetic operations

## Future Improvements

1. Implement API key authorization for secure access to the API endpoints
2. Add a `generate_random_number` function that generates a random number within a specified range