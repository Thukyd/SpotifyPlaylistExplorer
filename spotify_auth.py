import threading
import requests
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import webbrowser

# Event to signal when the access token has been fetched
access_token_fetched = threading.Event()

class SpotifyAuth:
    def __init__(self, config_path="./config.json"):
        # Load configuration from JSON file
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config.json: {e}")
            sys.exit(1)

        # Initialize Spotify API parameters
        self.client_id = config.get("client_id")
        self.client_secret = config.get("client_secret")
        self.redirect_uri = config.get("redirect_uri")
        self.scope = config.get("scope")

        # Initialize token variables
        self.access_token = None
        self.token_type = None
        self.expires_in = None
        self.refresh_token = None

    def generate_auth_url(self):
        # Generate the Spotify authorization URL
        base_url = "https://accounts.spotify.com/authorize"
        response_type = "code"
        auth_url = f"{base_url}?client_id={self.client_id}&response_type={response_type}&redirect_uri={self.redirect_uri}&scope={self.scope}"
        return auth_url

    def fetch_access_token(self, auth_code):
        # Fetch the access token using the authorization code
        token_url = "https://accounts.spotify.com/api/token"
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            token_info = json.loads(response.text)
            self.access_token = token_info['access_token']
            self.token_type = token_info['token_type']
            self.expires_in = token_info['expires_in']
            self.refresh_token = token_info.get('refresh_token')
            print("Access token fetched successfully")
        else:
            print(f"Failed to get access token: {response.text}")

    def start_oauth_flow(self):
        # Start the OAuth 2.0 flow
        auth_url = self.generate_auth_url()
        webbrowser.open(auth_url)
        
        # Create HTTP server and link it to the AuthHandler
        server = HTTPServer(('localhost', 8080), self.AuthHandler)
        server.spotify_instance = self  # Pass the SpotifyAuth instance to the AuthHandler

        # Run the server in a separate thread
        thread = threading.Thread(target=server.handle_request)
        thread.start()

    class AuthHandler(BaseHTTPRequestHandler):
        # HTTP handler for the OAuth 2.0 callback
        def do_GET(self):
            # Access the SpotifyAuth instance
            spotify = self.server.spotify_instance

            # Parse the GET request to get the authorization code
            query = urlparse(self.path).query
            query_components = parse_qs(query)
            auth_code = query_components['code'][0] if 'code' in query_components else None

            # If authorization code exists, fetch the access token
            if auth_code:
                spotify.fetch_access_token(auth_code)
                access_token_fetched.set()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Access token fetched successfully.')
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Failed to fetch access token.')

    def wait_for_token(self):
        # Wait until the access token is fetched
        access_token_fetched.wait()
