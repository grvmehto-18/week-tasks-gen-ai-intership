import streamlit as st

st.set_page_config(
    page_title="EV Insights Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Electric Vehicle (EV) Insights Dashboard")

st.markdown("""
Welcome to the EV Insights Dashboard! This platform is designed to provide a comprehensive analysis of the electric vehicle market.
You can navigate through different sections using the sidebar to explore various aspects of our project.

### 📄 Pages:
- **Prediction**: Predict the price of an electric vehicle based on its features.
- **EDA (Exploratory Data Analysis)**: Visualize the EV dataset with various plots and statistical summaries.
- **Chatbot**: Ask questions about the EV dataset and get answers from our intelligent chatbot.

### 🚀 Getting Started
Select a page from the sidebar to begin your exploration.
""")

# You can add more global configurations or introductory text here.