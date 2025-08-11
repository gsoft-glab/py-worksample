import gradio as gr
import requests

# API configuration
API_BASE_URL = "http://127.0.0.1:8000/api"
CONVERSATION_ID = None

def create_conversation():
    """
    Create a new conversation and store its ID globally.
    
    Returns:
        bool: True if successful, False otherwise
    """
    global CONVERSATION_ID
    try:
        response = requests.post(
            f"{API_BASE_URL}/conversations/",
            json={"title": "Gradio Chat", "owner_id": "gradio_user"}
        )
        response.raise_for_status()
        conversation_data = response.json()
        CONVERSATION_ID = conversation_data["id"]
        print(f"Created conversation with ID: {CONVERSATION_ID}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating conversation: {e}")
        return False

def send_message(message, owner_id="gradio_user"):
    """
    Send a message to the API.
    
    Args:
        message (str): The message content
        owner_id (str): The ID of the message owner
        
    Returns:
        Response: The API response
    """
    global CONVERSATION_ID
    
    print(f"Sending message to conversation {CONVERSATION_ID}: {message}")
    response = requests.post(
        f"{API_BASE_URL}/conversations/{CONVERSATION_ID}/messages",
        json={"content": message, "owner_id": owner_id}
    )
    
    print(f"Response status: {response.status_code}")
    return response

def extract_assistant_response(messages):
    """
    Extract the most recent assistant response from a list of messages.
    
    Args:
        messages (list): List of message objects
        
    Returns:
        str: The assistant's response or a default message
    """
    ai_messages = [msg for msg in messages if msg["sender"] == "assistant"]
    
    if ai_messages:
        latest_response = ai_messages[-1]["content"]
        print(f"Latest AI response: {latest_response}")
        return latest_response
    else:
        print("No AI response found")
        return "I'm processing your request..."

def respond(message, history):
    """
    Send a user message to the API and get the assistant's response.
    This is the main function used by the Gradio interface.
    
    Args:
        message (str): The user's message
        history (list): Chat history (managed by Gradio)
        
    Returns:
        str: The assistant's response
    """
    global CONVERSATION_ID
    
    # Create conversation if it doesn't exist
    if CONVERSATION_ID is None:
        if not create_conversation():
            return "Sorry, I couldn't connect to the AI service. Please try again later."
    
    try:
        # Send user message to API
        response = send_message(message)
        
        # Handle 404 error (conversation not found)
        if response.status_code == 404:
            print("Conversation not found (404). Creating a new conversation...")
            if not create_conversation():
                return "Sorry, I couldn't connect to the AI service. Please try again later."
            
            # Re-send the message after creating the conversation
            response = send_message(message)
            response.raise_for_status()
        else:
            response.raise_for_status()

        # Process the response
        messages = response.json()
        print(f"Retrieved {len(messages)} messages from response")
        return extract_assistant_response(messages)
            
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e}")
        return f"Sorry, there was an error communicating with the AI service: {str(e)}"

# Create a Gradio chat interface
demo = gr.ChatInterface(
    fn=respond,
    title="AI Assistant Chat",
    description="Ask me anything!",
    examples=["Can you get the weather for me?", "What time is it?", "Can you add 5 + 3 for me?"],
    theme="default"
)

# Launch the interface
if __name__ == "__main__":
    create_conversation()
    demo.launch()