# util.py
import pickle
import json
import pandas as pd

# Global variables to store model and metadata
__locations = None  # List of available locations
__data_columns = None  # All feature names used during model training
__model = None  # Loaded ML model


def get_estimated_price(location, sqft, bhk, bath):
    """
    Predict house price based on user inputs.
    """
    # Convert location to lowercase so it matches training column format
    location = location.strip().lower()

    # Try to find the location column index
    try:
        loc_index = __data_columns.index(location)
    except ValueError:
        loc_index = -1  # If location not found, keep -1 (no one-hot flag)

    # Create an empty dataframe with all columns = 0
    x = pd.DataFrame([[0] * len(__data_columns)], columns=__data_columns)

    # Fill numerical fields (must match training order)
    x.iloc[0, 0] = sqft
    x.iloc[0, 1] = bath
    x.iloc[0, 2] = bhk

    # Set location column to 1 (one-hot encoding)
    if loc_index >= 0:
        x.iloc[0, loc_index] = 1

    # Return model prediction (rounded to 2 decimals)
    return round(__model.predict(x)[0], 2)


def load_saved_artifacts():
    """
    Load the trained model + data columns from local artifact files.
    This function must be called before prediction.
    """
    print("loading saved artifacts...start")

    global __data_columns, __locations, __model

    # Load feature names (data columns) exactly as stored in training
    with open(
        r"D:/Machine_Learning_Codebasics/GitHub/Real_State_Price_Prediction/server/artifacts/columns.json",
        "r",
    ) as f:
        cols = json.load(f)["data_columns"]
        __data_columns = cols
        __locations = __data_columns[3:]  # Locations start after sqft, bath, bhk

    # Load trained ML model
    if __model is None:
        with open(
            r"D:/Machine_Learning_Codebasics/GitHub/Real_State_Price_Prediction/server/artifacts/karachi_home_prices_model.pickle",
            "rb",
        ) as f:
            __model = pickle.load(f)

    print("loading saved artifacts...done")


def get_location_names():
    """Return list of available locations for frontend dropdown."""
    return __locations


def get_data_columns():
    """Return all data columns (debug/inspection use only)."""
    return __data_columns


# Run tests only when file is executed directly
if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price("Orangi Town", 1000, 3, 3))
    print(get_estimated_price("Orangi Town", 1000, 2, 2))
    print(get_estimated_price("Gulshan-e-Iqbal", 1000, 2, 2))
    print(get_estimated_price("Clifton", 1000, 2, 2))
    print(get_estimated_price("North Nazimabad", 1000, 2, 2))
