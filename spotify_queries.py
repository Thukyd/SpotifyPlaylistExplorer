# OAuth2 Authentication Setup
import json
import os
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

    def load_or_fetch_playlists(self):
        """
        Retrieve the user's Spotify playlists, either from a cached JSON file or via an API call.
        
        This method first checks if the playlists are already cached in a JSON file.
        If they are, it reads the file and returns the playlists.
        If not, it makes an API call to fetch the playlists, caches them in a JSON file,
        and then returns them.
        
        Returns:
            playlists (list or dict): List of dictionaries, each containing information about a playlist.
        """
        # Define the path to the JSON file where the data will be stored
        file_path = './cache/users_playlists.json'
        
        # Create the 'cache' directory if it doesn't exist
        if not os.path.exists('./cache'):
            print("Creating 'cache' directory...")
            os.makedirs('./cache')
        
        # Check if the JSON file already exists
        if os.path.exists(file_path):
            print("Fetching playlists from cache...")
            # If it exists, read the file to get the stored data
            with open(file_path, 'r') as f:
                playlists = json.load(f)
        else:
            print("PLAYLIST NOT IN CACHE - MAKING AN API CALL")
            data = self.collect_all_playlists_for_user() 

            # If the data is a dictionary, try to get 'items'; otherwise, use data as is
            if isinstance(data, dict):
                print("Data is a dictionary. Fetching 'items' key.")
                playlists = data.get("items", [])
            else:
                print("Data is not a dictionary. Using data as-is.")
                playlists = data

            # Store the data in the JSON file
            with open(file_path, 'w') as f:
                json.dump(playlists, f)
        
        # Return the playlists, either from the file or the API
        return playlists


    def collect_all_playlists_for_user(self):
        """
        Collect all of the Spotify playlists for the current user.
        
        This function iteratively calls the Spotify API to fetch all playlists
        for the current user, handling pagination via 'limit' and 'offset' parameters.
        It returns a list containing all these playlists.
        
        Returns:
            all_playlists (list): List of dictionaries, each containing information about a playlist.
        """
        all_playlists = []
        limit = 50  # Maximum allowed by Spotify
        offset = 0  # Start at the beginning

        while True:
            logging.info(f"Fetching playlists, Offset: {offset}")
            
            # Fetch a batch of playlists
            playlists_batch = self.fetch_playlists_batch_from_api(limit=limit, offset=offset)

            # Check for failed fetch or end of playlists
            if playlists_batch is None or 'items' not in playlists_batch:
                logging.error("Failed to fetch playlists or reached the end.")
                break

            # Extend the list of all playlists with the new batch
            all_playlists.extend(playlists_batch['items'])
            logging.info(f"Fetched {len(playlists_batch['items'])} playlists in this batch.")

            # Check if we've reached the end of the playlists
            if len(playlists_batch['items']) < limit:
                logging.info("Reached the end of playlists.")
                break

            # Update the offset for the next batch
            offset += limit
            logging.info(f"Updating offset to {offset}")

        logging.info(f"Total playlists fetched: {len(all_playlists)}")
        return all_playlists

    def fetch_playlists_batch_from_api(self, limit, offset):
        """
        Fetch a batch of Spotify playlists for the current user from the Spotify API.
        
        Makes an API request to fetch a batch of playlists for the current user.
        The number of playlists fetched in each request is determined by the 'limit'
        parameter, starting at the 'offset'.
        
        Parameters:
            limit (int): The maximum number of playlists to return in each API call.
            offset (int): The index of the first playlist to return.
            
        Returns:
            dict or None: A dictionary containing the batch of playlists, or None if the request fails.
        """
        logging.info("Fetching current user's playlists...")
        endpoint = f"https://api.spotify.com/v1/me/playlists?limit={limit}&offset={offset}"
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

    def api_get_current_users_top_tracks(self):
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
