import requests
import time
import os

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

def get_response_from_api(api_url):
    """
    :param api_url: 
    :return: 
    """
    response = requests.get(api_url)
    destination_az = response.json()['availability_zone']
    return destination_az
    
def send_request():
    try:
        # Get the metadata token
        token = get_metadata_token()

        # Get the availability zone using the token
        source_az = get_availability_zone(token)
        api_url = os.environ['API_URL']
        while True:
            destination_az = get_response_from_api(api_url)
            print(f"Origin {source_az}, Destination: {destination_az}, Cross-AZ: {source_az != destination_az}, Server: {api_url}")
            time.sleep(5)
    except Exception as e:
        print(e)

# Run the application
if __name__ == '__main__':
    send_request()
