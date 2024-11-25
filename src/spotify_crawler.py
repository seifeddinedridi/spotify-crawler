import os
import time
from typing import List, Dict, Any

import spotipy
import yaml
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

from src.artist import Artist, Album


class SpotifyTunisianArtistCrawler:
    def __init__(self):
        load_dotenv()

        # Initialize Spotify client
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def search_tunisian_artists(self) -> list[Artist]:
        """Search for Tunisian artists on Spotify."""
        artists = []
        offset = 0
        limit = 50  # Maximum allowed by Spotify API

        # Search terms to find Tunisian artists
        search_queries = [
            'genre:raï location:tunisia',
            'genre:arab location:tunisia',
            'genre:rap location:tunisia',
            'genre:\"rap tunisien\" location:tunisia',
            'genre:\"arabic hip hop\" location:tunisia',
            'artist tunisia',
            'rap tunisien',
            'tunisian rap',
            'tunisian music',
        ]

        for query in search_queries:
            print(f"\nSearching with query: {query}")
            while True:
                try:
                    results = self.sp.search(
                        q=query,
                        type='artist',
                        limit=limit,
                        offset=offset
                    )

                    if not results['artists']['items']:
                        break

                    for artist in results['artists']['items']:
                        if self._is_likely_tunisian(artist):
                            artist_data = self.get_artist_details(artist['id'])
                            if artist_data:
                                artists.append(artist_data)
                                print(f"Found artist: {artist_data.name}")

                    offset += limit
                    time.sleep(1)  # Rate limiting

                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    time.sleep(5)
                    continue

        return artists

    def _is_likely_tunisian(self, artist: Dict[str, Any]) -> bool:
        """Check if an artist is likely to be Tunisian based on available data."""
        # This is a simple heuristic and could be improved
        if not artist.get('name'):
            return False

        tunisian_keywords = ['tunisia', 'tunisie', 'tunisian', 'tunis', 'rap tunisien']
        artist_name_lower = artist['name'].lower()

        # Check name and genres
        for keyword in tunisian_keywords:
            if keyword in artist_name_lower:
                return True

        if artist.get('genres'):
            for genre in artist['genres']:
                if any(keyword in genre.lower() for keyword in tunisian_keywords):
                    return True

        return False

    def get_artist_details(self, artist_id: str) -> Artist:
        yaml.emitter.Emitter.prepare_tag = lambda self, tag: ''
        """Get detailed information about an artist."""
        try:
            artist = self.sp.artist(artist_id)
            albums = self.sp.artist_albums(artist_id, album_type='album,single')

            album_list = []
            single_list = []

            # Categorize releases as albums or singles
            for album in albums['items']:
                release_date = album['release_date']
                if len(release_date) == 4:  # Only the year is present
                    release_date += '-01-01'
                album_info = Album(
                    name=album['name'],
                    release_date=release_date,
                    total_tracks=album['total_tracks'],
                    spotify_url=album['external_urls']['spotify']
                )

                if album['album_type'] == 'album':
                    album_list.append(album_info)
                else:
                    single_list.append(album_info)

            artist_data = Artist(
                name=artist['name'],
                spotify_handle=artist['id'],
                profile_photo_url=artist['images'][0]['url'] if artist['images'] else None,
                genres=artist['genres'],
                popularity=artist['popularity'],
                followers=artist['followers']['total'],
                spotify_url=artist['external_urls']['spotify'],
                albums=album_list,
                singles=single_list
            )

            return artist_data

        except Exception as e:
            print(f"Error getting details for artist {artist_id}: {str(e)}")
            return None

    def save_results(self, artists: List[Artist], output_dir: str = 'output'):
        """Save results in both YAML and CSV formats."""
        os.makedirs(output_dir, exist_ok=True)

        # Save as YAML
        class NoAliasDumper(yaml.Dumper):
            def ignore_aliases(self, data):
                return True
        yaml_path = os.path.join(output_dir, 'tunisian_artists.yaml')
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(artists, f, allow_unicode=True, default_flow_style=False, Dumper=NoAliasDumper)

        print(f"\nResults saved to {output_dir}/")
        print(f"Total artists found: {len(artists)}")

def main():
    crawler = SpotifyTunisianArtistCrawler()
    print("Starting Tunisian artist crawler...")
    artists = crawler.search_tunisian_artists()
    artists = sorted(artists, key=lambda x: x.popularity, reverse=True)
    crawler.save_results(artists)


def export_individual_artist():
    crawler = SpotifyTunisianArtistCrawler()
    artist = crawler.get_artist_details("3MKpGPhBp9KeXjGooKHNDX")
    crawler.save_results([artist])

if __name__ == "__main__":
    main()
    # export_individual_artist()
