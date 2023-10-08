# Spotify Playlist Explorer: My 10-Year Music Diary
# TODO: Update Docs - refactor without Spotipy usage
- direct API Usage instead of Spotioy https://developer.spotify.com/documentation/web-api
- OAuth 2.0 implementation
- Caching for playlists
- Refactoring to Data queries


## Introduction

What do you do when you've accumulated a decade's worth of carefully curated Spotify playlists, organized month by month? For me, it's not just a matter of hitting the shuffle button. Each playlist is a chapter in a 10-year musical journey, each one connected with vivid memories. However, I found no existing tools that could analyze these specific playlists in the way I wanted.

The Playlist Explorer aims to fill this gap for. Built on the Spotipy Library (Spotify API), the scropt queries playlists based on your criterias (for me some basic regex). It assembles data structures that include the complete track list, frequency of song appearances across playlists, most-added artists, and more. There are several pre-defined outputs which provide a chance to explore your musical history, offering insights that might give you some inspiration for new plyalists.

## Features

- Query all "diary" playlists that follow a specific naming pattern.
- More features to be added.

## Requirements

- Python 3.x
- Spotipy library
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
