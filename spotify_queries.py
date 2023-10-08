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

    def generate_auth_url(self):
        base_url = "https://accounts.spotify.com/authorize"
        response_type = "code"
        auth_url = f"{base_url}?client_id={self.client_id}&response_type={response_type}&redirect_uri={self.redirect_uri}&scope={self.scope}"
        return auth_url

    def fetch_access_token(self, auth_code):
        token_url = "https://accounts.spotify.com/api/token"
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            token_info = json.loads(response.text)
            self.access_token = token_info['access_token']
            self.token_type = token_info['token_type']
            self.expires_in = token_info['expires_in']
            self.refresh_token = token_info.get('refresh_token')
            print("Access token fetched successfully")
        else:
            print(f"Failed to get access token: {response.text}")

    def get_current_user_playlists(self):
        logging.info("Fetching current user's playlists...")
        endpoint = "https://api.spotify.com/v1/me/playlists"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            logging.info("Successfully fetched playlists.")
            return json.loads(response.text)
        elif response.status_code == 429:
            logging.error(f"Failed to fetch playlists due to rate limiting. More info: https://developer.spotify.com/documentation/web-api/concepts/rate-limits")
        else:
            logging.error(f"Failed to fetch playlists: {response.text}")
            return None

    def get_current_user_top_tracks(self):
        logging.info("Fetching current user's top tracks...")
        endpoint = "https://api.spotify.com/v1/me/top/tracks"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            logging.info("Successfully fetched top tracks.")
            return json.loads(response.text)
        elif response.status_code == 429:
            logging.error(f"Failed to fetch top tracks due to rate limiting. More info: https://developer.spotify.com/documentation/web-api/concepts/rate-limits")
        else:
            logging.error(f"Failed to fetch top tracks: {response.text}")
            return None
