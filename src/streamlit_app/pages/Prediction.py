import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import numpy as np

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.data_service import DataService
from src.models.regression import SimpleLinearRegressionModel, RandomForestRegressorModel

st.set_page_config(page_title="EV Price Prediction", page_icon="🔌")

st.title("EV Price Prediction")

st.markdown("""
This page allows you to predict the price of an electric vehicle in Germany (before incentives). 
Select a model and provide the necessary features to get a prediction.
""")

@st.cache_resource
def load_data_and_models():
    """
    Loads the data and trains the models.
    Using cache to avoid reloading and retraining on every interaction.
    """
    data_service = DataService(file_path='src/datasets/ev_raw_data.csv')
    data_service.load_data()
    data_service.clean_data()
    features, target = data_service.get_features_and_target()

    # Train Simple Linear Regression Model
    lr_model = SimpleLinearRegressionModel()
    lr_model.split_data(features, target)
    lr_model.train()
    lr_metrics = lr_model.evaluate()

    # Train Random Forest Regressor Model
    rf_model = RandomForestRegressorModel()
    rf_model.split_data(features, target)
    rf_model.train()
    rf_metrics = rf_model.evaluate()
    
    # Get the cleaned dataframe for UI selections
    df_for_ui = data_service.get_dataframe_for_eda()

    return lr_model, lr_metrics, rf_model, rf_metrics, features, df_for_ui

lr_model, lr_metrics, rf_model, rf_metrics, features, df_for_ui = load_data_and_models()

# Model Selection
model_choice = st.selectbox("Choose a regression model:", ("Simple Linear Regression", "Random Forest Regressor"))

st.header("Model Performance")
if model_choice == "Simple Linear Regression":
    st.write("Metrics for Simple Linear Regression:")
    st.json(lr_metrics)
else:
    st.write("Metrics for Random Forest Regressor:")
    st.json(rf_metrics)

st.header("Predict EV Price")

# --- Input fields for prediction ---
col1, col2 = st.columns(2)

with col1:
    make_options = sorted(df_for_ui['make'].unique())
    selected_make = st.selectbox("Make", options=make_options)
    
    model_options = sorted(df_for_ui[df_for_ui['make'] == selected_make]['model'].unique())
    selected_model = st.selectbox("Model", options=model_options)

    drive_config_options = sorted(df_for_ui['drive_config'].unique())
    selected_drive_config = st.selectbox("Drive Configuration", options=drive_config_options)

with col2:
    selected_battery = st.slider("Battery (kWh)", min_value=int(df_for_ui['battery'].min()), max_value=int(df_for_ui['battery'].max()), value=int(df_for_ui['battery'].mean()))
    selected_seats = st.selectbox("Number of Seats", options=sorted(df_for_ui['seats'].unique()))


if st.button("Predict Price"):
    # Create a dictionary with all possible feature columns, initialized to 0
    input_data_dict = {col: 0 for col in features.columns}
    
    # Set the user-provided values
    input_data_dict['battery'] = selected_battery
    input_data_dict['seats'] = selected_seats
    
    # Set the one-hot encoded columns based on user selection
    make_col = f"make_{selected_make}"
    if make_col in input_data_dict:
        input_data_dict[make_col] = 1
        
    model_col = f"model_{selected_model}"
    if model_col in input_data_dict:
        input_data_dict[model_col] = 1
        
    drive_config_col = f"drive_config_{selected_drive_config}"
    if drive_config_col in input_data_dict:
        input_data_dict[drive_config_col] = 1

    # Convert the dictionary to a DataFrame
    input_df = pd.DataFrame([input_data_dict])
    
    # Ensure the column order is the same as in the training data
    input_df = input_df[features.columns]

    # Make prediction
    with st.spinner('Predicting...'):
        if model_choice == "Simple Linear Regression":
            prediction = lr_model.predict(input_df)
        else:
            prediction = rf_model.predict(input_df)

    st.success(f"Predicted Price (Germany, before incentives): €{prediction[0]:,.2f}")