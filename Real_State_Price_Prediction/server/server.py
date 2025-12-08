# server.py
from flask import Flask, request, jsonify
import util

app = Flask(__name__)


# ---------------------------------------------
# API: Get all available location names
# ---------------------------------------------
@app.route("/get_location_names", methods=["GET"])
def get_location_names():
    response = jsonify({"locations": util.get_location_names()})
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow frontend access
    return response


# ---------------------------------------------
# API: Predict house price
# ---------------------------------------------
@app.route("/predict_home_price", methods=["GET", "POST"])
def predict_home_price():
    # Receive form inputs from frontend
    total_sqft = float(request.form["total_sqft"])
    location = request.form["location"]
    bhk = int(request.form["bhk"])
    bath = int(request.form["bath"])

    # Call prediction function
    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

    # Send response
    response = jsonify({"estimated_price": estimated_price})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# ---------------------------------------------
# Main: Start Flask server
# ---------------------------------------------
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()  # Load model before API starts
    app.run()
