import requests
import shutil

# Replace these values with your actual API key and external user IDx
API_KEY = "<izKwERgjpWcEUi28ZO13iXXtClpGkn2f>"
EXTERNAL_USER_ID = "<67fa76ad253882d386fe7346>"
BASE_URL = "https://api.on-demand.io/chat/v1"

def create_chat_session():
    """
    Create a chat session and return the session ID.
    """
    url = f"{BASE_URL}/sessions"
    headers = {
        "apikey": API_KEY
    }
    body = {
        "pluginIds": [],
        "externalUserId": EXTERNAL_USER_ID
    }
    
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 201:
        session_id = response.json().get("data", {}).get("id")
        return session_id
    else:
        raise Exception(f"Failed to create chat session: {response.status_code}, {response.text}")

def submit_query(session_id, query, response_mode="sync"):
    """
    Submit a query to the chat session.
    """
    url = f"{BASE_URL}/sessions/{session_id}/query"
    headers = {
        "apikey": API_KEY
    }
    body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": query,
        "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1718116202"],
        "responseMode": response_mode,
        "reasoningMode": "medium"
    }
    
    if response_mode == "sync":
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to submit query: {response.status_code}, {response.text}")
    elif response_mode == "stream":
        # Handle Server-Sent Events (SSE) using requests
        with requests.post(url, json=body, headers=headers, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        print(line.decode("utf-8"))
            else:
                raise Exception(f"Failed to submit query (stream mode): {response.status_code}, {response.text}")
    else:
        raise ValueError("Invalid response mode. Use 'sync' or 'stream'.")

if __name__ == "__main__":
    try:
        # Step 1: Create a chat session
        session_id = create_chat_session()
        print(f"Chat session created with ID: {session_id}")
        
        # Step 2: Submit a query (sync mode)
        query = "Put your query here"
        response = submit_query(session_id, query, response_mode="sync")
        print("Query response (sync mode):", response)
        
        # Step 3: Submit a query (stream mode)
        print("Query response (stream mode):")
        submit_query(session_id, query, response_mode="stream")
    except Exception as e:
        print("Error:", e)
