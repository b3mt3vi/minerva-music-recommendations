import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import musicbrainzngs
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))

# MusicBrainz API setup
musicbrainzngs.set_useragent("MusicRecommendationSystem", "0.1", "your_email@example.com")

def collect_lastfm_data(artist_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    data = response.json()
    artist_data = {
        'name': data['artist']['name'],
        'listeners': data['artist']['stats']['listeners'],
        'playcount': data['artist']['stats']['playcount'],
        'bio': data['artist']['bio']['summary']
    }
    return artist_data

def collect_musicbrainz_data(artist_name):
    result = musicbrainzngs.search_artists(artist=artist_name)
    artist_id = result['artist-list'][0]['id']
    
    # Get artist's releases
    releases = musicbrainzngs.browse_releases(artist=artist_id, includes=["recordings"], limit=5)
    release_data = []
    for release in releases['release-list']:
        release_data.append({
            'title': release['title'],
            'date': release['date'],
            'country': release.get('country', 'Unknown')
        })
    return release_data

def collect_spotify_data(artist_name):
    results = sp.search(q='artist:' + artist_name, type='artist')
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    
    # Get artist's albums
    albums = sp.artist_albums(artist_id, album_type='album')
    album_data = []
    for album in albums['items']:
        album_data.append({
            'album_name': album['name'],
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'spotify_url': album['external_urls']['spotify']
        })
    return album_data

def collect_data():
    artist_name = 'Radiohead'  # Example artist
    print(f"Collecting data for {artist_name}...")
    
    lastfm_data = collect_lastfm_data(artist_name)
    musicbrainz_data = collect_musicbrainz_data(artist_name)
    spotify_data = collect_spotify_data(artist_name)
    
    # Save data to CSV files
    lastfm_df = pd.DataFrame([lastfm_data])
    musicbrainz_df = pd.DataFrame(musicbrainz_data)
    spotify_df = pd.DataFrame(spotify_data)
    
    lastfm_df.to_csv('data/raw/lastfm_data.csv', index=False)
    musicbrainz_df.to_csv('data/raw/musicbrainz_data.csv', index=False)
    spotify_df.to_csv('data/raw/spotify_data.csv', index=False)

if __name__ == "__main__":
    collect_data()

