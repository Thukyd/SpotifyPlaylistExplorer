from spotify_queries import SpotifyQueries
from filter_and_analyse_data import FilterAndAnalyseData


# You can proceed with the rest of your code here.


########
## I.) Spotify Queries

# Initialize the Spotify API client with necessary credentials and scope
spotify_diary = SpotifyDiary(client_id, client_secret, redirect_uri, scope)


diary_playlists_tracks = spotify_diary.fetch_track_details_from_playlist()

########
## II.) Data Operations


# c) Find your most played songs out of the lists
#TODO: You have the data structure but you need a better way how to print this in Data Analysis
print(spotify_diary.filter_top_50_tracks(diary_playlists_tracks))


########
## III.) Visualisations


#TODOS:

# Function to find and print the top 10 songs in the filtered list, along with the playlists they appear in

# Function to find your most played songs out of the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the most played artists out of the artistst presented - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the top 5 songes for each of the months represented by the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find the most popular songs world wide from your selection - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter  

