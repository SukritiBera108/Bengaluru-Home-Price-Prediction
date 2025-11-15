import pickle
import json
import numpy as np
import os  # <-- 1. IMPORT OS

# 2. GET THE ABSOLUTE PATH TO THIS FILE'S DIRECTORY
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bath, bhk):
    """
    Predicts the price based on user input.
    """
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1 

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    # Format the price with "Lakhs"
    prediction = round(__model.predict([x])[0], 2)
    return prediction

def load_saved_artifacts():
    """
    Loads the saved model and column information from disk.
    """
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # 3. BUILD THE CORRECT FILE PATHS
    json_path = os.path.join(__location__, "artifacts/columns.json")
    model_path = os.path.join(__location__, "artifacts/banglore_home_prices_model.pickle")

    with open(json_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    if __model is None:
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
    
    print("loading saved artifacts...done")

def get_location_names():
    """
    Returns the list of location names.
    """
    # Ensure artifacts are loaded before trying to access
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

# --- THIS IS IMPORTANT ---
# Load the artifacts ONE time when the server starts
load_saved_artifacts()

if __name__ == '__main__':
    # This part only runs when you execute 'python util.py' directly
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))

