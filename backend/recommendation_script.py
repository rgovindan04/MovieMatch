import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset (adjust the path to your actual file)
movies = pd.read_csv('/Users/rishigovindan/the-movies-dataset/movies_metadata.csv', low_memory=False).fillna('')

# Preprocess the dataset
movies['combined_features'] = movies['genres'] + ' ' + movies['overview']
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_movies(title):
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

    if title not in indices:
        raise ValueError(f"Movie '{title}' not found in the dataset!")

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Exclude itself

    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()  # Return as a list
