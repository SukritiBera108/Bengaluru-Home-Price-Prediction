from flask import Flask, request, jsonify, render_template
from . import util  # Use the relative import

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def home():
    """Renders the home page."""
    # Pass request so the form can remember old values on first load
    return render_template('app.html', prediction_text='', is_error=False, request=request)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """Returns the list of locations to the front-end."""
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """
    Handles the form submission, predicts price, and renders the result.
    This is your function, which is correct.
    """
    try:
        # Get data from form
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Get raw number (e.g., 85.5) from util.py
        estimated_price = util.get_estimated_price(location, total_sqft, bath, bhk)

        if estimated_price > 0:
            if estimated_price >= 100:
                # Convert to Crores
                crore_value = estimated_price / 100
                prediction_text = f"Estimated Price: {crore_value:,.2f} Crore (INR)"
            else:
                # Keep in Lakhs
                prediction_text = f"Estimated Price: {estimated_price:,.2f} Lakh (INR)"
            is_error = False
        else:
            prediction_text = 'Invalid Input. Unrealistic House for that place.'
            is_error = True

    except (ValueError, KeyError):
        # Handle bad input (e.g., empty fields, non-numbers)
        prediction_text = 'Invalid User Input. Please check all fields.'
        is_error = True

    # Render the page again, now with the prediction_text
    return render_template(
        'app.html',
        prediction_text=prediction_text,
        is_error=is_error,
        request=request  # Pass request to remember form values
    )
