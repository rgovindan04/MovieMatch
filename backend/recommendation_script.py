import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib

# Define paths
DATASET_PATH = os.path.expanduser('/Users/rishigovindan/backend/movies_metadata.csv')
CACHE_DIR = os.path.expanduser('/Users/rishigovindan/backend/cache')

def preprocess_movies():
    # Create cache directory if it doesn't exist
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Load dataset
    movies = pd.read_csv(DATASET_PATH, low_memory=False)

    # Clean and preprocess
    movies = movies.fillna('')
    movies['combined_features'] = movies['genres'] + ' ' + movies['overview']
    movies['title'] = movies['title'].str.strip().str.title()

    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Save preprocessed data
    joblib.dump(movies, os.path.join(CACHE_DIR, 'movies_processed.pkl'))
    joblib.dump(tfidf, os.path.join(CACHE_DIR, 'tfidf.pkl'))
    joblib.dump(cosine_sim, os.path.join(CACHE_DIR, 'cosine_sim.pkl'))

def load_preprocessed_data():
    movies = joblib.load(os.path.join(CACHE_DIR, 'movies_processed.pkl'))
    tfidf = joblib.load(os.path.join(CACHE_DIR, 'tfidf.pkl'))
    cosine_sim = joblib.load(os.path.join(CACHE_DIR, 'cosine_sim.pkl'))
    return movies, tfidf, cosine_sim

def recommend_movies(title):
    # Check if preprocessed files exist, if not create them
    if not os.path.exists(os.path.join(CACHE_DIR, 'movies_processed.pkl')):
        preprocess_movies()

    # Load preprocessed data
    movies, tfidf, cosine_sim = load_preprocessed_data()

    # Create index mapping
    indices = pd.Series(movies.index, index=movies['title'].str.strip().str.title()).drop_duplicates()

    # Check if movie exists
    if title.strip().title() not in indices:
        raise ValueError(f"Movie '{title}' not found in the dataset!")

    # Get movie index
    idx = indices[title.strip().title()]

    # Compute similar movies
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] < len(movies) and movies['original_language'].iloc[score[0]] == 'en']
    sim_scores = sim_scores[:10]  # Get top 10 recommendations excluding itself

    # Get movie indices and titles
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()