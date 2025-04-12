import streamlit as st
import requests

# Plugin and endpoint constants
PLUGIN_IDS = ["plugin-1712327325", "plugin-1713962163", "plugin-1718116202"]
ENDPOINT_ID = "predefined-openai-gpt4o"
RESPONSE_MODE = "sync"
REASONING_MODE = "medium"

def create_chat_session(api_key, external_user_id):
    create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
    create_session_headers = {
        'apikey': api_key
    }
    create_session_body = {
        'pluginIds': [],  # Leave empty during creation
        'externalUserId': external_user_id
    }

    response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
    response_data = response.json()
    return response_data['data']['id']

def submit_query(api_key, session_id, query):
    submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    submit_query_headers = {
        'apikey': api_key
    }
    submit_query_body = {
        'endpointId': ENDPOINT_ID,
        'query': query,
        'pluginIds': PLUGIN_IDS,
        'responseMode': RESPONSE_MODE,
        'reasoningMode': REASONING_MODE
    }

    query_response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
    return query_response.json()

def main():
    # Input fields for the title and image URL
    title = st.text_input("Hansen Search Group Linkin Agent")
    image_url = st.text_input("https://media.licdn.com/dms/image/v2/C4E0BAQEH9HeXXfJdyg/company-logo_100_100/company-logo_100_100/0/1630598494090?e=1749686400&v=beta&t=o5UdqPe1Iz7lPmWj6DOigwNcgpdsTlxhMNCSGmziIAQ")

    # Display title and image
    st.title(title)
    st.image(image_url, use_column_width=True)

    # Sidebar for API key and external user ID
    st.sidebar.header("API Configuration")
    api_key = st.sidebar.text_input("Enter API Key", type="password")
    external_user_id = st.sidebar.text_input("Enter External User ID", type="password")

    if not api_key or not external_user_id:
        st.warning("Please enter your API key and external user ID in the sidebar.")
        return

    # Create session button
    if st.button("Create Chat Session"):
        with st.spinner("Creating chat session..."):
            try:
                session_id = create_chat_session(api_key, external_user_id)
                st.session_state['session_id'] = session_id
                st.success(f"Chat session created successfully. Session ID: {session_id}")
            except Exception as e:
                st.error(f"Error creating chat session: {str(e)}")

    # Query input and submit
    if 'session_id' in st.session_state:
        query = st.text_input("Enter your query")
        if st.button("Submit Query"):
            if query:
                with st.spinner("Submitting query..."):
                    try:
                        response = submit_query(api_key, st.session_state['session_id'], query)
                        st.json(response)
                    except Exception as e:
                        st.error(f"Error submitting query: {str(e)}")
            else:
                st.warning("Please enter a query.")
    else:
        st.info("Create a chat session first before submitting queries.")

if __name__ == "__main__":
    main()