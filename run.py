from src.data_collection import collect_data
from src.data_processing import process_data
from src.recommendation import build_annoy_index, generate_annoy_recommendations

def main():
    print("Starting data collection...")
    collect_data()

    print("Processing data...")
    process_data()

    print("Building Annoy index...")
    build_annoy_index()

    print("Generating recommendations...")
    recommendations = generate_annoy_recommendations(item_id=0)  # Example item_id
    print("Recommendations:", recommendations)

if __name__ == "__main__":
    main()

