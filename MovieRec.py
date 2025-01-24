import pandas as pd
movies = pd.read_csv('/Users/rishigovindan/Desktop/movies_metadata.csv', low_memory=False)
print(movies.head())

movies = movies.fillna('')

movies['combined_features'] = movies['genres'] + ' ' + movies['overview']

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_movies(title, cosine_sim=cosine_sim):
    # Create a mapping of movie titles to their indices
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

    # Check if the movie title exists in the dataset
    if title not in indices:
        return f"Movie '{title}' not found in the dataset!"

    # Get the index of the given movie
    idx = indices[title]

    # Get pairwise similarity scores for the movie
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Exclude the first entry (itself) and validate indices
    sim_scores = [score for score in sim_scores if score[0] < len(movies)]
    sim_scores = sim_scores[1:11]  # Top 10 recommendations excluding itself

    # Handle cases where there aren't enough similar movies
    if not sim_scores:
        return "Not enough similar movies found!", []

    # Get the indices of the top movies
    movie_indices = [i[0] for i in sim_scores]

    # Return the movie titles and indices for debugging
    return movies['title'].iloc[movie_indices], movie_indices


recommendations, movie_indices = recommend_movies('The Dark Knight')

# Print the recommendations
print(recommendations)

# Print the movie indices for debugging
print("Movie indices:", movie_indices)

# Print the number of movies in the dataset
print("Number of movies in dataset:", len(movies))

