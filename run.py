import argparse
from src.data_collection import collect_data
from src.data_processing import process_data
from src.recommendation import build_annoy_index, generate_annoy_recommendations

def main(artist_name, num_recommendations):
    print(f"Starting data collection for {artist_name}...")
    collect_data(artist_name)

    print("Processing data...")
    process_data()

    print("Building Annoy index...")
    build_annoy_index()

    print(f"Generating {num_recommendations} recommendations for {artist_name}...")
    recommendations = generate_annoy_recommendations(item_id=0, num_recommendations=num_recommendations)  # Example item_id
    print("Recommendations:\n", recommendations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music Recommendation System")
    parser.add_argument("artist_name", type=str, help="Name of the artist")
    parser.add_argument("num_recommendations", type=int, help="Number of recommendations")
    args = parser.parse_args()
    
    main(args.artist_name, args.num_recommendations)

