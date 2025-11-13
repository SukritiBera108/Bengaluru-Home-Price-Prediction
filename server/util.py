import pickle
import json
import numpy as np


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

   
    return round(__model.predict([x])[0], 2)

def load_saved_artifacts():
    """
    Loads the saved model and column information from disk.
    """
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

  
    with open("./server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
  
        __locations = __data_columns[3:]

    
    if __model is None:
        with open('./server/artifacts/banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    
    print("loading saved artifacts...done")

def get_location_names():
    """
    Returns the list of location names.
    """
    return __locations

def get_data_columns():
    """
    Returns the list of all data columns.
    """
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) 
    print(get_estimated_price('Ejipura', 1000, 2, 2)) 