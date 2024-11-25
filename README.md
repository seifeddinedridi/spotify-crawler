# Tunisian Artists Spotify Crawler

This project includes a Python script that crawls Spotify's API to find Tunisian artists and their music.

## Setup

1. Create a Spotify Developer account and get your API credentials:
   - Go to https://developer.spotify.com/dashboard
   - Create a new application
   - Get your Client ID and Client Secret

2. Set up your environment variables:
   ```bash
   export SPOTIFY_CLIENT_ID='your_client_id'
   export SPOTIFY_CLIENT_SECRET='your_client_secret'
   ```

3. Install the required Python package:
   ```bash
   pip install spotipy
   ```

4. Run the crawler:
   ```bash
   python src/scripts/spotify_crawler.py
   ```

The script will create a JSON file named `tunisian_artists.json` containing the artist information.

## Data Format

The crawler generates data in the following format:

```json
{
  "id": "spotify_id",
  "fullName": "Artist Name",
  "email": "generated_email",
  "profilePhotoUrl": "url_to_photo",
  "genres": ["genre1", "genre2"],
  "spotifyHandle": "spotify_id",
  "albums": [
    {
      "id": "album_id",
      "title": "Album Title",
      "releaseYear": 2023,
      "coverUrl": "url_to_cover"
    }
  ],
  "singles": [
    {
      "id": "single_id",
      "title": "Single Title",
      "releaseYear": 2023,
      "coverUrl": "url_to_cover"
    }
  ]
}
```

Note: The email addresses are generated based on the artist's name and are not real contact information.