class FilterAndAnalyseData:
    def __init__(self, pattern, all_playlists):
        self.pattern = pattern  # Regular expression pattern for filtering
        self.all_playlists = all_playlists  # All playlists to be filtered

    def get_filtered_playlists(self):
        logging.info("Filtering current user's playlists based on pattern...")

        if self.all_playlists is None:
            logging.error("No playlists provided for filtering.")
            return None

        # Initialize the list to store filtered playlists
        filtered_playlists = []

        # Loop through each playlist and apply the regex filter
        for playlist in self.all_playlists.get('items', []):
            if re.match(self.pattern, playlist['name']):
                logging.info(f"Match found: {playlist['name']}")
                filtered_playlists.append({
                    'name': playlist['name'],
                    'id': playlist['id']
                })

        logging.info(f"Successfully filtered {len(filtered_playlists)} playlists.")
        return filtered_playlists
