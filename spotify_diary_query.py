
# Importing required libraries
import spotipy
import json
import re
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict, Counter
import time


class SpotifyDiary:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            redirect_uri=redirect_uri,
                                            scope=scope
                                            ))
        
        # Regular expression pattern to filter playlists based on naming schema
        self.pattern = r'(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)(?: und (Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember))? \d{4} *- *+'


    def query_diary_playlists(self):
        print("Starting to fetch and filter playlists based on the pattern...")
        try:
            # Initialize variables
            filtered_playlists = []
            offset = 0
            batch_size = 50
            max_filtered = 100

            while True:
                print(f"About to make API call with offset {offset} and batch size {batch_size}...")
                try:
                    playlists = self.sp.current_user_playlists(offset=offset, limit=batch_size)["items"]
                    print(f"API call successful. Fetched {len(playlists)} playlists.")
                except Exception as api_error:
                    print(f"An error occurred during the API call: {api_error}")
                    return None

                if not playlists:
                    print("No more playlists to fetch. Breaking out of the loop.")
                    break

                for playlist in playlists:
                    if re.match(self.pattern, playlist['name']):
                        print(f"Match found: {playlist['name']}")
                        filtered_playlists.append({
                            'name': playlist['name'],
                            'id': playlist['id']
                        })

                    if len(filtered_playlists) >= max_filtered:
                        print(f"Reached max filtered limit of {max_filtered}. Stopping early.")
                        return filtered_playlists

                print(f"Completed this batch. {len(filtered_playlists)} playlists match the pattern so far.")
                offset += len(playlists)
                time.sleep(3)  # Small delay to prevent hitting rate limits

            print(f"Successfully fetched and filtered {len(filtered_playlists)} playlists.")
            return filtered_playlists

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def fetch_track_details_from_playlist(self):
        # Initialize the data structure to hold track details
        track_data = defaultdict(list)
        
        # Fetch and process each playlist
        playlists = self.query_diary_playlists()

        print("Fetching tracks from playlists...")
        for playlist in playlists:
            playlist_id = playlist['id']
            playlist_name = playlist['name']

            #print(f"Processing playlist: {playlist_name}")

            # Fetch tracks in the current playlist
            tracks = self.sp.playlist_tracks(playlist_id)["items"]
            for track_info in tracks:
                track = track_info.get('track', {})

                # Check if track is not None
                if track:
                    track_id = track.get('id', 'Unknown')
                    track_name = track.get('name', 'Unknown')
                    artist_name = track.get('artists', [{}])[0].get('name', 'Unknown')
                    
                    #print(f"Adding track: {track_name} by {artist_name}")

                    # Populate data structure
                    track_data[track_id].append({
                        'song_title': track_name,
                        'artist': artist_name,
                        'playlist': playlist_name
                    })
                else:
                    print(f"Warning: Encountered a track with no details. In Playlist {playlist_name}")
            
        print("Completed fetching track details.")
        return track_data
    
    def get_top_tracks_all_time(self):
        print("Starting to fetch top 50 tracks of all time...")
        try:
            top_tracks_data = {}
            # Get top tracks for the current user over the long term
            time_range = 'long_term'
            results = self.sp.current_user_top_tracks(limit=50, time_range=time_range)

            # Check if 'items' key exists in results
            if 'items' not in results:
                print("Error: 'items' key not found in the API response.")
                return None

            # Populate the top_tracks_data dictionary
            for idx, item in enumerate(results['items']):
                top_tracks_data[idx + 1] = {
                    'artist': item['artists'][0]['name'],
                    'track': item['name'],
                    'track_id': item['id']
                }
            print("Successfully fetched top 50 tracks of all time.")
            return top_tracks_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    
    # Method to filter top 50 favorite tracks based on their presence in other playlists
    def filter_top_50_tracks(self, playlist_tracks):
        print("Starting to filter Top 50 tracks based on playlist tracks...")
        try:
            # Fetch my top 50 songs of all time (not only from the diary)
            top_50_favorites = self.get_top_tracks_all_time()
            
            # Initialize a dictionary to hold the filtered top 50 tracks
            filtered_top_50 = {}
            
            # Loop through the top 50 favorites and check if they are in the playlist_tracks
            for rank, track_info in top_50_favorites.items():
                track_id = track_info['track_id']
                if track_id in playlist_tracks:
                    filtered_top_50[rank] = track_info
            
            print(f"Successfully filtered. {len(filtered_top_50)} tracks remain in the Top 50 list.")
            return filtered_top_50
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

#FIXME
"""
    def query_diary_playlists_songs(self, playlists_to_query):
        # Initialize data structures for storing playlist data and for frequency analysis
        playlist_data = defaultdict(list)
        artist_counter = Counter()
        song_counter = Counter()
        song_playlist_map = defaultdict(set)

        # Loop through filtered playlists to fetch tracks and their details
        for playlist in playlists_to_query:
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            
            tracks = self.sp.playlist_tracks(playlist_id)['items']
            
            # Check for None values and store track details
            for track in tracks:
                if track is None or track['track'] is None:
                    continue
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                track_id = track['track']['id']
                
                playlist_data[playlist_name].append({
                    'title': track_name, 
                    'artist': artist_name,
                    "track_id": track_id,
                    'playlist_id': playlist_id
                })
                
                # Update frequency counters and mappings
                artist_counter[artist_name] += 1
                song_counter[track_name] += 1
                song_playlist_map[track_name].add(playlist_name)

        # Loop through filtered playlists to fetch tracks and their details
        for playlist in playlists_to_query:
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            
            # print(f"\n=== Fetching Tracks for Playlist: {playlist_name} ===")
            
            tracks = self.sp.playlist_tracks(playlist_id)['items']
            
            # Check for None values and store track details
            for track in tracks:
                if track is None or track['track'] is None:
                    print("  - (Empty or None track encountered)")
                    continue
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                track_id = track['track']['id']
                
                #print(f"  - {track_name} by {artist_name}")
                
                playlist_data[playlist_name].append({
                    'title': track_name, 
                    'artist': artist_name,
                    "track_id": track_id,
                    'playlist_id': playlist_id
                })
                
                # Update frequency counters and mappings
                artist_counter[artist_name] += 1
                song_counter[track_name] += 1
                song_playlist_map[track_name].add(playlist_name)

        return playlist_data, song_playlist_map, artist_counter, song_counter

 """