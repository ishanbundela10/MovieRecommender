import os
import pickle
from pathlib import Path

import requests
import streamlit as st


POSTER_FALLBACK = "https://placehold.co/500x750?text=No+Poster"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
DATA_DIR = Path(__file__).resolve().parent


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_poster(movie_id, api_key):
    if not api_key:
        return POSTER_FALLBACK

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    try:
        response = requests.get(
            url,
            params={"api_key": api_key, "language": "en-US"},
            timeout=10,
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"  
    except (requests.exceptions.RequestException, ValueError):
        pass

    return POSTER_FALLBACK


def recommend(movie_title, movies, similarity, api_key, result_count=5):
    matching_movies = movies.index[movies["title"] == movie_title]
    if matching_movies.empty:
        return []

    movie_index = matching_movies[0]
    ranked_movies = sorted(
        enumerate(similarity[movie_index]),
        key=lambda item: item[1],
        reverse=True,
    )
    recommendations = []

    for index, _ in ranked_movies:
        if index == movie_index:
            continue

        movie = movies.iloc[index]
        recommendations.append(
            (movie["title"], fetch_poster(movie["movie_id"], api_key))
        )
        if len(recommendations) == result_count:
            break

    return recommendations


def load_recommender_data():
    try:
        with (DATA_DIR / "movie_list.pkl").open("rb") as movie_file:
            movies = pickle.load(movie_file)
        with (DATA_DIR / "similarity.pkl").open("rb") as similarity_file:
            similarity = pickle.load(similarity_file)
    except (OSError, pickle.PickleError, EOFError, ImportError, ModuleNotFoundError, ValueError) as error:
        st.error(f"Could not load the recommender data: {error}")
        st.stop()

    required_columns = {"title", "movie_id"}
    if not required_columns.issubset(movies.columns):
        st.error("The movie data must contain 'title' and 'movie_id' columns.")
        st.stop()
    if len(movies) != len(similarity):
        st.error("The movie list and similarity data do not match. Rebuild the recommender files.")
        st.stop()

    return movies.reset_index(drop=True), similarity


st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.title("Movie Recommender")
st.caption("Find films with a similar story and feel.")

movies, similarity = load_recommender_data()
if not TMDB_API_KEY:
    st.info("Set the TMDB_API_KEY environment variable to show movie posters.")

selected_movie = st.selectbox(
    "Choose a movie",
    movies["title"].tolist(),
)

if st.button("Show recommendations", type="primary"):
    recommendations = recommend(selected_movie, movies, similarity, TMDB_API_KEY)
    if not recommendations:
        st.info("No similar movies were found.")
    else:
        for column, (title, poster) in zip(st.columns(len(recommendations)), recommendations):
            with column:
                st.image(poster, use_container_width=True)
                st.caption(title)