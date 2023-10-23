# OAuth2 Authentication Setup
import json
import os
import requests
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

class SpotifyQueries:
    def __init__(self, access_token):
        self.access_token = access_token

    def cached_data_available(self, file_name):
        """
        Check if the user's Spotify data is already cached in a JSON file.

        Parameters:
            file_name (str): The name of the file to check for in the cache.

        Returns:
            bool: True if the data is cached (i.e., file exists), False otherwise.
        """

        # If the file_name already contains the cache directory path, use it as is.
        # Otherwise, append the cache directory path to the file_name.
        print(f"Checking cached_data_available for file: {file_name}")
        file_path = f'./cache/{file_name}.json'

        # Check if the file exists in the cache directory
        if os.path.exists(file_path):
            # print(f"File exists: True")
            return True
        else:
            # print(f"File exists: False")
            return False


    def load_cached_data(self, file_name):
        """
        Load the user's Spotify data from a cached JSON file.
        
        Parameters:
            file_name (str): The name of the JSON file to read from the cache.
            
        Returns:
            dict: The data read from the JSON file.
            
        Raises:
            FileNotFoundError: If the specified JSON file does not exist in the cache.
        """

        # Define the path to the JSON file where the data will be stored
        file_path = f'./cache/{file_name}.json'
        
        # Check if the JSON file already exists
        if self.cached_data_available(file_name):
            print("Spotify data in cache - Reading from file")
            # Read the cached data from the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        else:
            raise FileNotFoundError(f"No cached data found at {file_path}")

# TODO: Think about if you want to invalidate the cache after a certain amount of time
    def cache_data(self, data, file_name):
        """
        Cache the user's Spotify data in a JSON file.
        
        Parameters:
            data (dict or list): Data to be cached, which can be a dictionary or a list of dictionaries.
            file_name (str): The name of the JSON file where the data will be stored.
        """

        # Create the 'cache' directory if it doesn't exist
        if not os.path.exists('./cache'):
            print("Creating 'cache' directory...")
            os.makedirs('./cache')
        
        # Define the path to the JSON file where the data will be stored
        file_path = f'./cache/{file_name}.json'
        
        # Write the cached data to the JSON file
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print("Spotify data cached successfully.")
        
    
    def load_or_fetch_playlists(self):
        """
        Retrieve the user's Spotify playlists. If cached data is available, it reads from the cache;
        otherwise, it fetches the data via an API call and then caches it.
        
        Returns:
            list: A list of dictionaries, each containing information about a playlist.
        """

        # Define the path to the JSON file where the data will be stored
            #file_path = './cache/users_playlists.json'
        file_name = "users_playlists"

        if self.cached_data_available(file_name):
            print("Spotify playlist data in cache - Reading from file")
            # Read the cached data from the JSON file
            playlists = self.load_cached_data(file_name)
            return playlists
        else:
            print("Fetching Spotify playlist data via API...")
            playlists = self.collect_all_playlists_for_user()
            # Cache the playlists in a JSON file
            self.cache_data(playlists, file_name)
            return playlists
        
    def load_or_fetch_top_tracks(self):
        """
        Retrieve the user's Spotify playlists. If cached data is available, it reads from the cache;
        otherwise, it fetches the data via an API call and then caches it.
        
        Returns:
            list: A list of dictionaries, each containing information about a playlist.
        """

        # Define the path to the JSON file where the data will be stored
            #file_path = './cache/users_playlists.json'
        file_name = "users_top_tracks"

        if self.cached_data_available(file_name):
            print("Spotify top tracks data in cache - Reading from file")
            # Read the cached data from the JSON file
            top_tracks = self.load_cached_data(file_name)
            return top_tracks
        else:
            print("Fetching Spotify top tracks data via API...")
            top_tracks = self.api_get_current_users_top_tracks()
            # Cache the playlists in a JSON file
            self.cache_data(top_tracks, file_name)
            return top_tracks


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
            logging.error(f"Failed to fetch playlists. Error {response.status_code}: {response.text}")
            return None

# FIXME: Error for this mehtod:
# TODO: add logic which only adds the tracks if they are not already in the list and the snapshot_id is different
    def fetch_playlist_tracks_batch(self, query_playlists):
        fetched_playlists = []
        ## go through each Id of playlis
        # TODO: logic here
        for id in query_playlists:
            # inside of loop
            fetched_playlists.append(self.fetch_playlist_tracks(id))
        self.cache_data(fetched_playlists, "fetched_playlists_tracks")
        return fetched_playlists
        
    def fetch_playlist_tracks(self, playlist_id):
        """
        Fetch the tracks for a given playlist from the Spotify API.
        
        Parameters:
            playlist_id (str): The ID of the playlist to fetch.
            fields (str): The fields to return for each track.
            
        Returns:
            dict or None: A dictionary containing the playlist's tracks if successful, or None if the request fails.
        """
        logging.info(f"Fetching tracks for playlist ID {playlist_id}...")
        # filter of dates we want to use - https://developer.spotify.com/documentation/web-api/reference/get-playlist 
        fields = "id,name,tracks.items(track(artists(name, id, genres), name, id, popularity, album (name, id, release_date)))"
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}?fields={fields}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            logging.info("Successfully fetched tracks.")
            #self.cache_data(json.loads(response.text), playlist_id); # just for debugging
            return json.loads(response.text)
        elif response.status_code == 429:
            logging.error(f"Failed to fetch tracks due to rate limiting. More info: https://developer.spotify.com/documentation/web-api/concepts/rate-limits")
        else:
            logging.error(f"Failed to fetch tracks. Error {response.status_code}: {response.text}")
            return None    


# FIXME: There is a 403 error when trying to fetch the top tracks
#    NOTE: This is not an implementation error of this method. Others reported the same.
#    FIXME: Do you need to add the params for limit and time range? => might be the solution
    # https://stackoverflow.com/questions/75368571/cant-figure-out-auth-error-for-spotify-api-in-python-seeming-randomly-getting
    # https://stackoverflow.com/questions/62945183/error-403-when-trying-to-control-playback-on-another-device-through-spotipy-libr 
    # https://stackoverflow.com/questions/76675885/spotify-api-responding-with-error-code-403-when-requesting-top-songs-of-a-user
    def api_get_current_users_top_tracks(self):
        """
        Fetches the current user's top tracks from Spotify. Handles rate limiting and logs the status of the API call.
        
        Returns:
            dict or None: A dictionary containing the user's top tracks if successful, or None if the request fails.
        """

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
            logging.error(f"Failed to fetch top tracks. Error {response.status_code}: {response.text}")
            return None
