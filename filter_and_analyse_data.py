import os
import json
import logging
import re

class FilterAndAnalyseData:
    def __init__(self, pattern, all_playlists):
        self.pattern = pattern  # Regular expression pattern for filtering
        self.all_playlists = all_playlists  # All playlists to be filtered

    def cache_data(self, data, file_name):
        """
        Cache the user's Spotify data in a JSON file.
        
        Parameters:
            data (dict or list): Data to be cached.
            file_name (str): The name of the JSON file where the data will be stored.
        """
        if not os.path.exists('./cache'):
            print("Creating 'cache' directory...")
            os.makedirs('./cache')
        
        file_path = f'./cache/{file_name}.json'
        
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        print("Data cached successfully.")

    def load_cached_data(self, file_name):
        """
        Load cached data from a JSON file.
        
        Parameters:
            file_name (str): The name of the JSON file where the data is stored.
        
        Returns:
            dict or list: The cached data.
        """
        file_path = f'./cache/{file_name}.json'
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return data
    
    def get_filtered_playlists(self):
        logging.info("Filtering current user's playlists based on pattern...")

        if self.all_playlists is None:
            logging.error("No playlists provided for filtering.")
            return None

        # Initialize an empty list to store filtered playlists
        filtered_playlists = []

        # Your filtering logic here, for example:
        for playlist in self.all_playlists:
            if re.search(self.pattern, playlist['name']):
                filtered_playlists.append(playlist)

        # Cache the filtered playlists
        self.cache_data(filtered_playlists, "filtered_playlists")
        
        return filtered_playlists
    
    def get_top_10_songs(self):
        # TODO: you need to get the song details of each playlist first 
        # take in json file with playlists
        # find the top 10 songs appearing in the playlists
        # create a json structure which contains the track name, artist and a list of playlists it appears in
        # save the top 10 songs in a json file

        logging.info("Finding top 10 songs in filtered playlists...")

        # Load the filtered playlists from cache
        try:
            filtered_playlists = self.load_cached_data("filtered_playlists")
        except:
            logging.error("No filtered playlists found in cache for finding top 10 songs.")
            return None

        # Initialize an empty list to store top 10 songs
        top_10_songs = []

        # Your logic here, for example:
        for playlist in filtered_playlists:
            for track in playlist['tracks']:
                if track['track']['name'] not in top_10_songs:
                    top_10_songs.append(track['track']['name'])

        # Cache the top 10 songs
        self.cache_data(top_10_songs, "top_10_songs")
        
        return top_10_songs
    