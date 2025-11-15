import pickle
import json
import numpy as np
import os

# --- This block builds the correct, absolute paths ---
# Get the directory where this util.py file is located
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Build paths to the artifact files inside that directory
JSON_PATH = os.path.join(__location__, "artifacts/columns.json")
MODEL_PATH = os.path.join(__location__, "artifacts/banglore_home_prices_model.pickle")
# --- End of path block ---

# Global variables to hold the loaded model and columns
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bath, bhk):
    """
    Predicts the price based on user input.
    Returns the raw number (e.g., 85.5), NOT the formatted string.
    """
    try:
        # Find the index for the location
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # Location not found
        loc_index = -1 

    # Create the input array for the model
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1 # Set the location column to 1

    # Get the raw prediction (e.g., 85.5)
    prediction = round(__model.predict([x])[0], 2)
    return prediction # <-- SOLUTION: Returns the raw number

def load_saved_artifacts():
    """
    Loads the saved model and column information from disk using the correct paths.
    """
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Use the correct path to open columns.json
    with open(JSON_PATH, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:] # First 3 are sqft, bath, bhk

    # Use the correct path to open the model
    if __model is None:
        with open(MODEL_PATH, 'rb') as f:
            __model = pickle.load(f)
    
    print("Loading saved artifacts...done")

def get_location_names():
    """
    Returns the list of location names.
    """
    if __locations is None:
        load_saved_artifacts()
    return __locations

def get_data_columns():
    """
    Returns the list of all data columns.
    """
    if __data_columns is None:
        load_saved_artifacts()
    return __data_columns

# --- Load artifacts when the server starts ---
# This ensures the model is ready BEFORE the first request
load_saved_artifacts()
