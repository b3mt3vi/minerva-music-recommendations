import pandas as pd
from annoy import AnnoyIndex
import os

def build_annoy_index():
    print("Building Annoy index...")

    # Ensure the models directory exists
    if not os.path.exists('models'):
        os.makedirs('models')

    # Load processed data
    combined_df = pd.read_csv('data/processed/processed_data.csv')

    # Extract features for Annoy
    feature_columns = ['listeners', 'playcount', 'danceability', 'energy', 'valence', 'popularity', 'tempo', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    features = combined_df[feature_columns].fillna(0).values
    num_features = features.shape[1]

    # Initialize Annoy index
    index = AnnoyIndex(num_features, 'angular')

    # Add items to the index
    for i, feature_vector in enumerate(features):
        index.add_item(i, feature_vector)

    # Build the index
    index.build(10)  # Number of trees
    index.save('models/annoy_index.ann')

def generate_annoy_recommendations(item_id, num_recommendations=10):
    # Load the Annoy index
    combined_df = pd.read_csv('data/processed/processed_data.csv')
    feature_columns = ['listeners', 'playcount', 'danceability', 'energy', 'valence', 'popularity', 'tempo', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    num_features = len(feature_columns)

    index = AnnoyIndex(num_features, 'angular')
    index.load('models/annoy_index.ann')
    
    # Get similar items
    similar_items = index.get_nns_by_item(item_id, num_recommendations)
    
    # Map item IDs back to artist data
    recommendations = combined_df.iloc[similar_items]
    return recommendations

def get_recommendations(artist_name, num_recommendations=10):
    # Load processed data
    combined_df = pd.read_csv('data/processed/processed_data.csv')

    # Find the index of the artist
    artist_index = combined_df.index[combined_df['name'] == artist_name].tolist()
    if not artist_index:
        print(f"Artist {artist_name} not found in the dataset.")
        return

    # Generate recommendations
    recommendations = generate_annoy_recommendations(artist_index[0], num_recommendations)
    print("Recommendations:\n", recommendations)

if __name__ == "__main__":
    # Build the Annoy index
    build_annoy_index()

    # Example usage
    get_recommendations("Elis Regina", 5)

