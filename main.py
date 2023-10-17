# Import necessary modules
from spotify_queries import SpotifyQueries 
from filter_and_analyse_data import FilterAndAnalyseData
from http.server import HTTPServer, BaseHTTPRequestHandler  # For capturing the authorization code
from urllib.parse import urlparse, parse_qs  # For parsing URL and query strings
import json  # For loading the configuration file
import sys  # For exiting the program
import webbrowser  # For opening the web browser
import threading  # For running the HTTP server in a separate thread and for threading.Event

########
## I. Loading Configs & Initialise Spotify

# Load configuration from a JSON file
try:
    with open("./config.json", "r") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading config.json: {e}")
    sys.exit(1)

# Initialize Spotify API connection with loaded configuration
client_id = config.get("client_id")
client_secret = config.get("client_secret")
redirect_uri = config.get("redirect_uri")
scope = config.get("scope")
spotify = SpotifyQueries(client_id, client_secret, redirect_uri, scope)

########
## II. OAuth 2.0 Flow

# Create an event to signal when the access token is fetched
access_token_fetched = threading.Event()

# Function to get the authorization code from Spotify
# TODO: Make the loggings better. Don't give out the deubg logs here
# TODO: Externalize 
def get_auth_code():
    # Custom handler to process incoming HTTP GET requests
    class AuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Parse the query parameters from the URL
            query = urlparse(self.path).query
            query_components = parse_qs(query)
            
            # Extract the authorization code from the query parameters
            auth_code = query_components["code"][0] if "code" in query_components else None
            
            if auth_code:
                #print(f"Authorization code: {auth_code}")
                
                # Fetch the access token using the authorization code
                spotify.fetch_access_token(auth_code)
                
                # Set the event to signal that the access token has been fetched
                access_token_fetched.set()
                
                # Send an HTTP 200 response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Access token fetched successfully.')
            else:
                # Handle the case where the authorization code is not found
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Failed to fetch access token.')
    
    # Initialize HTTP server with custom handler
    server = HTTPServer(('localhost', 8080), AuthHandler)
    
    # Run the HTTP server in a separate thread to handle a single request
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    # Open the Spotify authorization URL in the default web browser
    auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    webbrowser.open(auth_url)
    

# Fetch the authorization code
get_auth_code()

# Wait for the access token to be fetched before continuing
access_token_fetched.wait()

########
## III. Query Spotify


# This code checks for a file named spotify_playlists.json in the current directory. If the file exists, it reads the playlists from there. 
# Otherwise, it calls the spotify.get_current_user_playlists() function to fetch the data, and then it stores that data in the spotify_playlists.json file for future use.
playlist = spotify.load_or_fetch_playlists()

# DEBUG: uncomment to print the playlist
#print(playlist) 

# TODO: Check if this still works
    # [ ] It should create a seperate json file
    # [ ] Use the same chaching mechanism as for the playlists
#spotify.get_current_user_top_tracks()


########
## IV.) Data Operations

# Create an instance of the FilterAndAnalyseData class
#TODO: use patern to find the date in the playlist name - think about where to store this? Directly here in the code? In the config file?
pattern = r'(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)(?: und (Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember))? \d{4} *- *+'
#spotify_diary = FilterAndAnalyseData()



# c) Find your most played songs out of the lists
#TODO: You have the data structure but you need a better way how to print this in Data Analysis
#print(spotify_diary.filter_top_50_tracks(diary_playlists_tracks))


########
## V.) Visualisations


# TODO: Function to find and print the top 10 songs in the filtered list, along with the playlists they appear in

# TODO: Function to find your most played songs out of the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# TODO: Function to find out the most played artists out of the artistst presented - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# TODO: Function to find out the top 5 songes for each of the months represented by the lists - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter

# TODO: Function to find the most popular songs world wide from your selection - possible inputs: playlist_songs, song_appearance, artist_counter, song_counter  

