# server.py
# Flask server to expose face recognition model as a REST API

from flask import Flask, request, jsonify
import util

# Create Flask application
app = Flask(__name__)


@app.route("/classify_image", methods=["GET", "POST"])
def classify_image():
    """
    API endpoint to classify an image sent from frontend.

    Expected Input:
    - image_data: Base64 encoded image (from HTML/JS frontend)

    Returns:
    - JSON response containing predicted class and probabilities
    """

    # Get base64 image data from form request
    image_data = request.form["image_data"]

    # Call utility function to classify image
    response = jsonify(util.classify_image(image_data))

    # Enable CORS (allows frontend to access backend API)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":

    print("Starting Python Flask Server For Sports Celebrity Image Classification")

    # Load trained model and class dictionary
    util.load_saved_artifacts()

    # Start Flask server on port 5000
    app.run(port=5000)
