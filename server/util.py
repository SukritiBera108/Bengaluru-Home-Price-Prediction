import pickle
import json
import numpy as np
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

JSON_PATH = os.path.join(__location__, "artifacts/columns.json")
MODEL_PATH = os.path.join(__location__, "artifacts/banglore_home_prices_model.pickle")

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bath, bhk):
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

    prediction = round(__model.predict([x])[0], 2)
    return prediction 
def load_saved_artifacts():
  
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    with open(JSON_PATH, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:] 
        
    if __model is None:
        with open(MODEL_PATH, 'rb') as f:
            __model = pickle.load(f)
    
    print("Loading saved artifacts...done")

def get_location_names():
    
    if __locations is None:
        load_saved_artifacts()
    return __locations

def get_data_columns():
    
    if __data_columns is None:
        load_saved_artifacts()
    return __data_columns

load_saved_artifacts()

