# Import necessary modules
from spotify_auth import SpotifyAuth  # Import the SpotifyAuth class
from spotify_queries import SpotifyQueries 
from filter_and_analyse_data import FilterAndAnalyseData

########
## I. OAuth 2.0 Flow for Spotify Web API

# Initialize SpotifyAuth
spotify_auth = SpotifyAuth()

# Start OAuth flow
spotify_auth.start_oauth_flow()

# Wait for the token to be fetched
spotify_auth.wait_for_token()

# Access the token
access_token = spotify_auth.access_token



########
## II. Query Spotify


# This code checks for a file named spotify_playlists.json in the current directory. If the file exists, it reads the playlists from there. 
# Otherwise, it calls the spotify.get_current_user_playlists() function to fetch the data, and then it stores that data in the spotify_playlists.json file for future use.

# TODO: introduce time based caching => do that before you go trough the whole OAuth flow again
#    - split the load / fatch and introduce the caching library
#    - this should be the first check: are there any chaached jsons and are they up-to-date
#    - for playlists you can make use of the snapshot functionality instead of time-stamps
#    - when the check is done, this should be part of the config that is loaded into the class spotify
#    - everytime there is new caching, the config should be updated
#    Acceptance criteria: if i delete a cached part, it the config should recognize that. => rethink the implementation strategy

spotify = SpotifyQueries(access_token) # Initialize SpotifyQueries with the access token

playlist = spotify.load_or_fetch_playlists()

# DEBUG: uncomment to print the playlist
#print(playlist) 

# TODO: don't load all of user 
top_tracks = spotify.load_or_fetch_top_tracks()
# DEBUG: uncomment to print the playlist
#print(top_tracks)


########
## III. Filter and Analyse Data
# Create an instance of the FilterAndAnalyseData class
#TODO: use patern to find the date in the playlist name - think about where to store this? Directly here in the code? In the config file?
pattern = r'(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)(?: und (Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember))? \d{4} *- *+'

# handover all the playlists and the pattern to filter
filtered_data = FilterAndAnalyseData(pattern, playlist)
# filter through the plalists and save it in cache
spotify_diary = filtered_data.get_filtered_playlists()
# get the song details for each of the playlists
# FIXME: still an error in the batch operation
# TODO: There is also a snapshot_id => use that maybe for caching in reduce the calls 
spotify_diary_tracks = spotify.fetch_playlist_tracks_batch(spotify_diary)

# find top 10 songs in playlist
# TODO: base is here but you need to get the song details for each of the spotify diary playlists first
#top_10_songs = filtered_data.get_top_10_songs()





# c) Find your most played songs out of the lists
#TODO: Fix bug above first -  You have the data structure but you need a better way how to print this in Data Analysis
#print(spotify_diary.filter_top_50_tracks(diary_playlists_tracks))


########
## IV.) Visualisations


# TODO: Function to find and print the top 10 songs in the filtered list, along with the playlists they appear in
#print(top_10_songs)

# TODO: Function to find your most played songs out of the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# TODO: Function to find out the most played artists out of the artistst presented - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# TODO: Function to find out the top 5 songes for each of the months represented by the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# TODO: Function to find the most popular songs world wide from your selection  => there is a param: "popularity": 43, in the spotify api

# TODO: Add tracks base on some audio features. 
#   See also: https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
