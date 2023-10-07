from spotify_queries import SpotifyQueries
from filter_and_analyse_data import FilterAndAnalyseData
import json

########
## I.) Spotify Queries

# Load Configs
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


# Initialise Spotify connection
spotify = SpotifyQueries(client_id, client_secret, redirect_uri, scope)
spotify.authenticate()

# Get Spotify data 
""" TODO:
Use the snapshot_id
Playlist APIs expose a snapshot_id that corresponds to the version of the playlist that you are working with.
Downloading a playlist can be expensive so some apps may want to store and
refer to the snapshot_id to avoid refreshing an entire playlist that has not changed.
You can learn more about snapshot_id in our Working with Playlists guide.
https://developer.spotify.com/documentation/web-api/concepts/playlists 
"""
print(spotify.get_current_user_playlists())


"""
OLD!!
# Initialize the Spotify API client with necessary credentials and scope
spotify_diary = SpotifyDiary(client_id, client_secret, redirect_uri, scope)


diary_playlists_tracks = spotify_diary.fetch_track_details_from_playlist()

"""

########
## II.) Data Operations


# c) Find your most played songs out of the lists
#TODO: You have the data structure but you need a better way how to print this in Data Analysis
#print(spotify_diary.filter_top_50_tracks(diary_playlists_tracks))


########
## III.) Visualisations


#TODOS:

# Function to find and print the top 10 songs in the filtered list, along with the playlists they appear in

# Function to find your most played songs out of the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the most played artists out of the artistst presented - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the top 5 songes for each of the months represented by the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find the most popular songs world wide from your selection - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter  

