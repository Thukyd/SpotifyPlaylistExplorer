# OAuth2 Authentication Setup
import json
import requests
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

class SpotifyQueries:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.access_token = None
        self.token_type = None
        self.expires_in = None
        self.refresh_token = None

    def authenticate(self):
        auth_url = "https://accounts.spotify.com/api/token"
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }
        auth_response = requests.post(auth_url, data=auth_data)
        if auth_response.status_code == 200:
            auth_info = json.loads(auth_response.text)
            self.access_token = auth_info['access_token']
            self.token_type = auth_info['token_type']
            self.expires_in = auth_info['expires_in']
            self.refresh_token = auth_info.get('refresh_token')
        else:
            print("Authentication failed:", auth_response.text)


def get_current_user_playlists(self):
    logging.info("Fetching current user's playlists...")
    # Define the API endpoint and headers for authentication
    endpoint = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {self.access_token}"}

    # Make the API request
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        logging.info("Successfully fetched playlists.")
        return json.loads(response.text)
    else:
        logging.error(f"Failed to fetch playlists: {response.text}")
        return None
    
def get_playlist_tracks(self, playlist_id):
    logging.info(f"Fetching tracks for playlist ID: {playlist_id}...")
    # Define the API endpoint and headers for authentication
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {self.access_token}"}

    # Make the API request
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        logging.info(f"Successfully fetched tracks for playlist ID: {playlist_id}.")
        return json.loads(response.text)
    else:
        logging.error(f"Failed to fetch tracks for playlist ID: {playlist_id}. Error: {response.text}")
        return None

def get_current_user_top_tracks(self):
    logging.info("Fetching current user's top tracks...")
    # Define the API endpoint and headers for authentication
    endpoint = "https://api.spotify.com/v1/me/top/tracks"
    headers = {"Authorization": f"Bearer {self.access_token}"}

    # Make the API request
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        logging.info("Successfully fetched top tracks.")
        return json.loads(response.text)
    else:
        logging.error(f"Failed to fetch top tracks: {response.text}")
        return None

