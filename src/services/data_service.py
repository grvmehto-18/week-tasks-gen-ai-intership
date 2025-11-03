
import pandas as pd
import numpy as np
from typing import Tuple

class DataService:
    """
    Service layer for handling data loading, cleaning, and preparation.
    Follows a repository pattern where data is loaded from a source (CSV).
    """

    def __init__(self, file_path: str):
        """
        Initializes the DataService with the path to the dataset.

        Args:
            file_path (str): The path to the EV dataset CSV file.
        """
        self.file_path = file_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """
        Loads the dataset from the specified file path.

        Returns:
            pd.DataFrame: The loaded pandas DataFrame.
        """
        print("Loading data...")
        self.df = pd.read_csv(self.file_path, low_memory=False)
        print("Data loaded successfully.")
        return self.df


    def clean_data(self) -> pd.DataFrame:
        """
        Performs data cleaning on the loaded DataFrame.
        This includes handling missing values and dropping irrelevant columns.

        Returns:
            pd.DataFrame: The cleaned pandas DataFrame.
        """
        if self.df is None:
            self.load_data()
        print(f"Initial shape: {self.df.shape}")

        print("Cleaning data...")
        # Rename columns to be more Python-friendly
        self.df.rename(columns={
            'price-range': 'price_range',
            '0 - 100': 'acceleration_0_100',
            'Top Speed': 'top_speed',
            'Range*': 'range',
            'Efficiency*': 'efficiency',
            'Fastcharge*': 'fastcharge',
            'Germany_price_before_incentives': 'price_de',
            'Netherlands_price_before_incentives': 'price_nl',
            'UK_price_after_incentives': 'price_uk',
            'Drive_Configuration': 'drive_config',
            'Tow_Hitch': 'tow_hitch',
            'Towing_capacity_in_kg': 'towing_capacity',
            'Number_of_seats': 'seats'
        }, inplace=True)

        # Extract Make from title
        self.df['make'] = self.df['title'].apply(lambda x: x.split(' ')[0])

        # For the purpose of price prediction, we need 'price_de'. Rows without it are not useful.
        self.df.dropna(subset=['price_de'], inplace=True)
        print(f"Shape after dropping rows with missing price_de: {self.df.shape}")
        
        # Drop columns that are not useful for price prediction.
        self.df.drop(['Row_ID', 'title', 'price_range', 'price_nl', 'price_uk'], axis=1, inplace=True)
        print(f"Shape after dropping irrelevant columns: {self.df.shape}")

        # Convert numerical columns from string to number, coercing errors
        for col in ['battery', 'acceleration_0_100', 'top_speed', 'range', 'efficiency', 'fastcharge', 'towing_capacity']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        print(f"Shape after converting to numeric: {self.df.shape}")

        # Fill missing values with the mean for numerical columns
        for col in self.df.select_dtypes(include=np.number).columns:
            self.df[col].fillna(self.df[col].mean(), inplace=True)
        print(f"Shape after filling NaNs with mean: {self.df.shape}")
        
        # Drop rows with any remaining missing values in other key columns
        self.df.dropna(inplace=True)
        print(f"Shape after final dropna: {self.df.shape}")

        print("Data cleaning complete.")
        return self.df

    def get_features_and_target(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separates the DataFrame into features (X) and target (y).
        The target for this project is 'price_de'.

        Returns:
            Tuple[pd.DataFrame, pd.Series]: A tuple containing the features DataFrame
                                             and the target Series.
        """
        if self.df is None:
            raise ValueError("Data not loaded or cleaned yet. Call load_data() and clean_data() first.")

        # We will predict 'price_de'.
        features = self.df.drop('price_de', axis=1)
        target = self.df['price_de']

        # One-hot encode categorical features
        features = pd.get_dummies(features, drop_first=True)

        return features, target

    def get_dataframe_for_eda(self) -> pd.DataFrame:
        """
        Returns a cleaned DataFrame suitable for EDA.

        Returns:
            pd.DataFrame: The cleaned pandas DataFrame.
        """
        if self.df is None:
            self.load_data()
            self.clean_data()
        return self.df

