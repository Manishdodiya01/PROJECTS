import pickle
import streamlit as st
import requests
from cachetools import cached, TTLCache

# Create a TTL (Time-To-Live) cache with a maximum size and expiration time
cache = TTLCache(maxsize=100, ttl=3600)  # Cache expires after 1 hour

@cached(cache)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path, data  # Return poster path and movie data

def imdb_link(movie_id):
    return f"https://www.imdb.com/title/{movie_id}/"

def recommend(movie):
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_data = []

    if movie in movies['title'].values:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:11]:
            # fetch the movie poster and data
            movie_id = movies.iloc[i[0]].movie_id
            poster_path, movie_data = fetch_poster(movie_id)
            recommended_movie_posters.append(poster_path)
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_data.append(movie_data)
    else:
        st.warning("Movie not found. Please enter a valid movie title.")

    return recommended_movie_names, recommended_movie_posters, recommended_movie_data

# Load data
movies = pickle.load(open("movie_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))

st.header('Movie Recommender System')

search_query = st.text_input("Search for a movie")

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_data = recommend(search_query)
    num_recommendations = len(recommended_movie_names)
    num_columns = 5
    num_rows = (num_recommendations + num_columns - 1) // num_columns
    
    for i in range(num_rows):
        row = st.columns(num_columns)
        for j in range(num_columns):
            idx = i * num_columns + j
            if idx < num_recommendations:
                with row[j]:
                    # Display clickable image
                    if st.image(recommended_movie_posters[idx], width=200, caption=recommended_movie_names[idx], use_column_width=True):
                        # Create link to IMDb page
                        imdb_url = imdb_link(recommended_movie_data[idx]['imdb_id'])
                        st.markdown(f"[ALL INFORMATION]({imdb_url})")
                        
                        # Add red box with more information
                        with st.expander("About Movie", expanded=False):
                            st.write(recommended_movie_data[idx]['overview'])
                            st.write(f"Release Date: {recommended_movie_data[idx]['release_date']}")
