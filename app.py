from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# IBM Watson ML credentials
API_KEY = "trpXJ-CN0ElEcGJ4aSkEUZqe0DeG5hKVr22Ib6Tg6nC-"
TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
ML_ENDPOINT = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/82e2be67-2e76-4bc6-8a5b-739327ac2689/predictions?version=2021-05-01"

# Get access token from IBM Watson
def get_ibm_token():
    token_response = requests.post(
        TOKEN_URL,
        data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return token_response.json()["access_token"]

# Route to receive area and return price prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        area = float(data.get("area", 0))

        mltoken = get_ibm_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + mltoken
        }

        payload = {
            "input_data": [
                {
                    "fields": ["Area (sq ft)"],
                    "values": [[area]]
                }
            ]
        }

        response = requests.post(ML_ENDPOINT, json=payload, headers=headers)
        prediction = response.json()["predictions"][0]["values"][0][0]

        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
