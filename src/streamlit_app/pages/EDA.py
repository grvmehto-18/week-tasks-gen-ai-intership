
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.data_service import DataService
from src.utils.eda import EDAUtils

st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📊")

st.title("Exploratory Data Analysis (EDA)")

st.markdown("""
This page displays various visualizations to help understand the EV dataset.
""")

@st.cache_data
def load_data():
    """
    Loads the data for EDA.
    """
    data_service = DataService(file_path='src/datasets/ev_raw_data.csv')
    df = data_service.get_dataframe_for_eda()
    return df

df = load_data()

st.header("Dataset Overview")
st.dataframe(df.head())

st.header("Descriptive Statistics")
st.write(df.describe())

st.header("Visualizations")



# Distribution of Price (Germany)
st.subheader("Distribution of Price (Germany, before incentives)")
with st.spinner("Generating plot..."):
    fig = EDAUtils.plot_distribution(df, 'price_de')
    st.pyplot(fig)

# Top 10 EV Makes
st.subheader("Top 10 EV Makes")
with st.spinner("Generating plot..."):
    fig = EDAUtils.plot_top_makes(df, top_n=10)
    st.pyplot(fig)

# Distribution of Drive Configurations
st.subheader("Distribution of Drive Configurations")
with st.spinner("Generating plot..."):
    fig = EDAUtils.plot_drive_config_distribution(df)
    st.pyplot(fig)

# Correlation Heatmap
st.subheader("Correlation Heatmap of Numerical Features")
with st.spinner("Generating plot..."):
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    fig = EDAUtils.plot_correlation_heatmap(df, numerical_cols)
    st.pyplot(fig)
