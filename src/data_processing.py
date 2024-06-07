import pandas as pd
from sklearn.preprocessing import StandardScaler

def process_data():
    print("Processing collected data...")
    
    # Load raw data
    lastfm_df = pd.read_csv('data/raw/lastfm_data.csv')
    musicbrainz_df = pd.read_csv('data/raw/musicbrainz_data.csv')
    spotify_df = pd.read_csv('data/raw/spotify_data.csv')
    
    # Merge datasets
    combined_df = pd.concat([lastfm_df, musicbrainz_df, spotify_df], axis=1)
    
    # Handle missing values
    combined_df.fillna(0, inplace=True)
    
    # Ensure columns exist
    feature_columns = ['listeners', 'playcount', 'danceability', 'energy', 'valence']
    for col in feature_columns:
        if col not in combined_df:
            combined_df[col] = 0
    
    # Extract and scale features
    scaler = StandardScaler()
    combined_df[feature_columns] = scaler.fit_transform(combined_df[feature_columns])
    
    # Save processed data
    combined_df.to_csv('data/processed/processed_data.csv', index=False)

if __name__ == "__main__":
    process_data()

