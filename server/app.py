from flask import Flask, jsonify
import requests
import os

# Create a Flask application instance
app = Flask(__name__)

# Function to get the AWS metadata token
def get_metadata_token():
    token_url = 'http://169.254.169.254/latest/api/token'
    headers = {
        'X-aws-ec2-metadata-token-ttl-seconds': '21600'
    }
    response = requests.put(token_url, headers=headers, timeout=2)
    response.raise_for_status()  # Raise an error for HTTP errors
    return response.text

# Function to get the availability zone using the metadata token
def get_availability_zone(token):
    metadata_url = 'http://169.254.169.254/latest/meta-data/placement/availability-zone'
    headers = {
        'X-aws-ec2-metadata-token': token
    }
    response = requests.get(metadata_url, headers=headers, timeout=2)
    response.raise_for_status()  # Raise an error for HTTP errors
    return response.text

# Define a route for the /availability-zone endpoint
@app.route('/az', methods=['GET'])
def get_availability_zone_endpoint():
    try:
        # Get the metadata token
        token = get_metadata_token()
        # Get the availability zone using the token
        availability_zone = get_availability_zone(token)

        # Return a JSON response with the availability zone
        print(f"Response from {availability_zone}")

        # Return a JSON response with the availability zone
        return jsonify(availability_zone=availability_zone)
    except requests.RequestException as e:
        # Handle potential errors (e.g., network issues, timeouts)
        return jsonify(error=str(e)), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
