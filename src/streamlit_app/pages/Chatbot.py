import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import os

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.chatbot_service import ChatbotService

def chatbot_page():
    """
    Renders the chatbot page.
    """
    st.title("EV Chatbot")

    # Input fields for API key, model name, and base URL
    with st.sidebar:
        st.header("API Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        model_name = st.text_input("Model Name", value="deepseek/deepseek-chat-v3.1:free")
        base_url = st.text_input("Base URL (e.g., OpenRouter)", value="https://openrouter.ai/api/v1")

        if not openai_api_key:
            st.warning("Please enter your OpenAI API Key to use the chatbot.")
            st.stop()


    # Load data
    @st.cache_data
    def load_data():
        """
        Loads the EV raw data from the CSV file.
        """
        return pd.read_csv("src/datasets/ev_raw_data.csv")

    df = load_data()

    # Initialize chatbot service
    @st.cache_resource
    def load_chatbot_service(api_key: str, model: str, url: str):
        """
        Initializes and caches the ChatbotService.
        """
        return ChatbotService(df, api_key, model, url)

    chatbot = load_chatbot_service(openai_api_key, model_name, base_url)

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about electric vehicles"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chatbot.ask_question(prompt)
                st.markdown(response["answer"])
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

if __name__ == "__main__":
    chatbot_page()