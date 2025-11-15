from flask import Flask, request, jsonify, render_template
from . import util  
app = Flask(__name__, static_url_path="/static")

@app.route('/')
def home():
    
    return render_template('app.html', prediction_text='', is_error=False, request=request)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
   
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
   
    try:
        
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, bath, bhk)

        if estimated_price > 0:
            if estimated_price >= 100:
               
                crore_value = estimated_price / 100
                prediction_text = f"Estimated Price: {crore_value:,.2f} Crore (INR)"
            else:
             
                prediction_text = f"Estimated Price: {estimated_price:,.2f} Lakh (INR)"
            is_error = False
        else:
            prediction_text = 'Invalid Input. Unrealistic House for that place.'
            is_error = True

    except (ValueError, KeyError):
        
        prediction_text = 'Invalid User Input. Please check all fields.'
        is_error = True

   
    return render_template(
        'app.html',
        prediction_text=prediction_text,
        is_error=is_error,
        request=request  
    )

