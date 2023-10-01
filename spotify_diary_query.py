
# Importing required libraries
import spotipy
import json
import re
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict, Counter


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

    def get_top_tracks_all_time(self):
        top_tracks_data = {}
        # Get top tracks for the current user over the long term
        time_range = 'long_term'
        results = self.sp.current_user_top_tracks(limit=50, time_range=time_range)

        # Populate the top_tracks_data dictionary
        for idx, item in enumerate(results['items']):
            top_tracks_data[idx + 1] = {
                'artist': item['artists'][0]['name'],
                'track': item['name'],
                'track_id': item['id']
            }
        return top_tracks_data


    def query_diary_playlists(self):
        # Initialize an empty list to hold filtered playlists
        filtered_playlists = []

        # Fetch and filter user's playlists based on the regex pattern
        offset = 0
        while True:
            playlists = self.sp.current_user_playlists(offset=offset)["items"]
            if not playlists:
                break

            for playlist in playlists:
                if re.match(self.pattern, playlist['name']):
                    filtered_playlists.append({
                        'name': playlist['name'],
                        'id': playlist['id']
                    })

            offset += len(playlists)
        return filtered_playlists


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
