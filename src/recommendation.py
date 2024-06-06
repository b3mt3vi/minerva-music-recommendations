import os
import pandas as pd
from annoy import AnnoyIndex

def build_annoy_index():
    print("Building Annoy index...")

    # Ensure the models directory exists
    if not os.path.exists('models'):
        os.makedirs('models')

    # Load processed data
    combined_df = pd.read_csv('data/processed/processed_data.csv')

    # Extract features for Annoy (example: just using listeners and playcount)
    features = combined_df[['listeners', 'playcount']].values
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
    num_features = 2  # Adjust to the actual number of features used in build_annoy_index

    index = AnnoyIndex(num_features, 'angular')
    index.load('models/annoy_index.ann')
    
    # Get similar items
    similar_items = index.get_nns_by_item(item_id, num_recommendations)
    
    # Map item IDs back to artist data
    recommendations = combined_df.iloc[similar_items]
    return recommendations

if __name__ == "__main__":
    print("Building Annoy index...")
    build_annoy_index()

    print("Generating recommendations...")
    recommendations = generate_annoy_recommendations(item_id=0)  # Example item_id
    print("Recommendations:\n", recommendations)

