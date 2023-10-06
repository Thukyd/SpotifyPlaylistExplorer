from spotify_diary_query import SpotifyDiary
import json
import sys

try:
    # Load credentials from config.json
    with open("config.json", "r") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading config.json: {e}")
    sys.exit(1)

client_id = config.get("client_id")
client_secret = config.get("client_secret")
redirect_uri = config.get("redirect_uri")
scope = config.get("scope")

# You can proceed with the rest of your code here.


########
## I.) Spotify Data Structure

# Initialize the Spotify API client with necessary credentials and scope
spotify_diary = SpotifyDiary(client_id, client_secret, redirect_uri, scope)
# a) get all of your diary playlists
# TODO: You are using the query_diary twice in your code. Maybe it's not needed. Find a better way.
#diary_playlists = spotify_diary.query_diary_playlists()
#print(diary_playlists)

diary_playlists_tracks = spotify_diary.fetch_track_details_from_playlist()
print(diary_playlists_tracks)

# b) Get more sepcifc data
# FIXME: This is not a good strcuture - please refactor "query_diary_playlists_songs"

"""
    playlist_songs: 
        {'September 2023 - Me and The Devil': [{'title': 'Me And The Devil', 'artist': 'Gil Scott-Heron', 'track_id': '76lCwB3Bu4tNcyXRLGvVba', 'playlist_id': '2boyaY9beajILnHZnzYJTD'},  ...
    song_appearance: 
        {'Me And The Devil': {'Februar 2014 - Down in the music hole', 'September 2023 - Me and The Devil', 'März 2014 - Dig deeper in the whole.'}, ...
    artist_counter:
        {'JAY-Z': 38, 'Chefket': 30, 'Tyler, The Creator': 28, ....
    song_counter:
        {'Let U Know': 10, 'Love Will Tear Us Apart': 10, 'Goodbye (feat. Lyse) - Radio Edit': 10, 'Easy': 10, ...
"""
# playlist_songs, song_appearance, artist_counter, song_counter = spotify_diary.query_diary_playlists_songs(diary_playlists)


# c) Find your most played songs out of the lists
#TODO: You have the data structure but you need a better way how to print this in Data Analysis
print(spotify_diary.filter_top_50_tracks(diary_playlists_tracks))


########
## II.) Visualisations


#TODOS:

# Function to find and print the top 10 songs in the filtered list, along with the playlists they appear in

# Function to find your most played songs out of the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the most played artists out of the artistst presented - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the top 5 songes for each of the months represented by the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find the most popular songs world wide from your selection - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter  

