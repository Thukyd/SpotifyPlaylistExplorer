# Spotify Playlist Explorer: My 10-Year Music Diary

## Introduction

What do you do when you've accumulated a decade's worth of carefully curated Spotify playlists, organized month by month? For me, it's not just a matter of hitting the shuffle button. Each playlist is a chapter in a 10-year musical journey, each one connected with vivid memories. However, I found no existing tools that could analyze these specific playlists in the way I wanted.

The Playlist Explorer aims to fill this gap for. Built on the [Spotify API](https://developer.spotify.com/documentation/web-api)
, the script queries playlists based on your criterias (for me some basic regex). It assembles data structures that include the complete track list, frequency of song appearances across playlists, most-added artists, and more. There are several pre-defined outputs which provide a chance to explore your musical history, offering insights that might give you some inspiration for new plyalists.

## Features

- OAuth 2.0 Authentication
- Direct API calls to Spotify
- Caching for API results
- Query all "diary" playlists that follow a specific naming pattern.

## Todos

- [ ] Query tracks of all filtered playlists
- [ ] Additional data analysis features
- [ ] Visualizations

## Requirements

- Python 3.x
- Spotify API credentials

## Configuration

The script uses a regular expression pattern to filter playlists based on their naming schema. In my case, all my playlists follow a certain naming convention, and I've tailored the regex accordingly. You'll likely want to update this pattern to match your own naming conventions:

```python
self.pattern = r'(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)(?: und (Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember))? \d{4} *- *+'
```

## Setup

1. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Add your Spotify API credentials to `config.json`:

   ```json
   {
     "client_id": "your_client_id_here",
     "client_secret": "your_client_secret_here",
     "redirect_uri": "your_redirect_uri_here",
     "scope": "playlist-read-private, user-top-read"
   }
   ```

3. Run the main script:

   ```bash
   python main.py
   ```

## Scripts Overview

### main.py

This is the entry point of the application. It imports necessary modules and sets up an HTTP server for capturing OAuth tokens.

- I. Loading Configs & Initialise Spotify
- II. OAuth 2.0 Flow
- III. Query Spotify
- IV. Analyse Data
- V. Visualisations

### spotify_queries.py

This script handles all the Spotify API queries and OAuth2 authentication.

### filter_and_analyse_data.py

Contains a class \`FilterAndAnalyseData\` which is used for advanced data filtering and analysis.
