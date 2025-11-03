"""
Streamlit Main App
This is the main entry point for the Streamlit application.
It sets up the main page and navigation.
"""
import streamlit as st
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(
        page_title="EV Analysis and Chatbot",
        page_icon="🚗",
        layout="wide",
    )

    st.sidebar.title("Navigation")
    st.sidebar.info(
        """
        Select a page from the dropdown above to navigate to different sections of the app.
        """
    )

    st.title("Electric Vehicle Analysis and Chatbot")
    st.write("Welcome to the EV Analysis and Chatbot app. Please select a page from the sidebar to get started.")

if __name__ == "__main__":
    main()
