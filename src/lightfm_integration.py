import pandas as pd
from lightfm import LightFM
from lightfm.data import Dataset
import pickle

def train_lightfm():
    # Load processed data
    data = pd.read_csv('data/processed/processed_data.csv')

    # Prepare data for LightFM
    dataset = Dataset()
    users = data['user_id'].unique()
    items = data['track_id'].unique()
    dataset.fit(users, items)

    (interactions, weights) = dataset.build_interactions([(x['user_id'], x['track_id']) for _, x in data.iterrows()])

    # Initialize and train model
    model = LightFM(loss='warp')
    model.fit(interactions, epochs=30, num_threads=2)

    # Save model
    with open('models/lightfm_model.pkl', 'wb') as f:
        pickle.dump(model, f)

def generate_lightfm_recommendations(user_id, num_recommendations=10):
    # Load model
    with open('models/lightfm_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Load data
    data = pd.read_csv('data/processed/processed_data.csv')
    item_mapping = {i: item for i, item in enumerate(data['track_id'].unique())}
    
    # Generate recommendations
    n_users, n_items = model.shape
    scores = model.predict(user_id, np.arange(n_items))
    top_items = np.argsort(-scores)[:num_recommendations]
    
    recommendations = [item_mapping[item_id] for item_id in top_items]
    return recommendations

if __name__ == "__main__":
    train_lightfm()

