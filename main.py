from spotify_diary_query import SpotifyDiary
import json

# Load credentials from config.json
with open("config.json", "r") as f:
    config = json.load(f)

client_id = config["client_id"]
client_secret = config["client_secret"]
redirect_uri = config["redirect_uri"]
scope = config["scope"]


########
## I.) Spotify Data Structure

# Initialize the Spotify API client with necessary credentials and scope
spotify_diary = SpotifyDiary(client_id, client_secret, redirect_uri, scope)
# a) get all of your diary playlists
diary_playlists = spotify_diary.query_diary_playlists()

# b) Get more sepcifc data
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
playlist_songs, song_appearance, artist_counter, song_counter = spotify_diary.query_diary_playlists_songs(diary_playlists)

# Scope are all tracks - not necesarily of my diary
# FIXME: 
#   There is still an error. Also think how to optimize. Do you really need all the data? I don't think so. Track_Id should be sufficent to kickout the tracks later.
my_top_track_all_time = spotify_diary.get_top_tracks_all_time()
print(my_top_track_all_time)

# TODO: 
#   Add another method in Spotify which gives you fast to be processes list of track Ids. This can be later used to kick out all tracks which are not part of your diary



########
## II.) Data Analysis


# Function to find and print the top 10 artists in the filtered list, along with their tracks and playlists
def print_top_10_artists(playlist_songs, artist_counter):
    print("\n=== Top 10 Artists in Filtered Playlists ===")
    for artist, count in artist_counter.most_common(10):
        print(f"{artist} (appears {count} times)")
        artist_tracks = []
        artist_playlists = set()
        for playlist, tracks in playlist_songs.items():
            for track in tracks:
                if track['artist'] == artist:
                    artist_tracks.append(track['title'])
                    artist_playlists.add(playlist)
        print(f"  Tracks: {', '.join(artist_tracks)}")
        print(f"  Playlists: {', '.join(artist_playlists)}")

# Function to find and print the top 10 songs in the filtered list, along with the playlists they appear in
def print_top_10_songs(song_counter, song_appearance):
    print("\n=== Top 10 Songs in Filtered Playlists ===")
    for song, count in song_counter.most_common(10):
        print(f"{song} (appears {count} times)")
        print(f"  Playlists: {', '.join(song_appearance[song])}")

########
## III.) Report


# Call the functions to print the top 10 artists and songs
#print_top_10_artists(playlist_songs, artist_counter)
#print_top_10_songs(song_counter, song_appearance)



#TODOS:

# Function to find your most played songs out of the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the most played artists out of the artistst presented - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find out the top 5 songes for each of the months represented by the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# Function to find the most popular songs world wide from your selection - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter  

