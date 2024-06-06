import pandas as pd

def process_data():
    print("Processing collected data...")
    
    # Load raw data
    lastfm_df = pd.read_csv('data/raw/lastfm_data.csv')
    musicbrainz_df = pd.read_csv('data/raw/musicbrainz_data.csv')
    spotify_df = pd.read_csv('data/raw/spotify_data.csv')
    
    # Example processing: merging the datasets
    combined_df = pd.concat([lastfm_df, musicbrainz_df, spotify_df], axis=1)
    
    # Save processed data
    combined_df.to_csv('data/processed/processed_data.csv', index=False)

if __name__ == "__main__":
    process_data()

