import pickle
import gzip

# Compress similarity.pkl
with open('similarity.pkl', 'rb') as f_in:
    with gzip.open('similarity.pkl.gz', 'wb') as f_out:
        f_out.writelines(f_in)

# Compress movies (1).pkl
with open('movies (1).pkl', 'rb') as f_in:
    with gzip.open('movies (1).pkl.gz', 'wb') as f_out:
        f_out.writelines(f_in)

print("Files compressed as 'similarity.pkl.gz' and 'movies (1).pkl.gz'")
import streamlit as st
import pickle
import gzip
import pandas as pd

def recommend(movie):
    # Find the movie index from the DataFrame
    movie_index = movies_data[movies_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    # Collect the recommended movie titles
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies_data.iloc[i[0]].title)
    return recommended_movies

# Load similarity matrix from compressed file
try:
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("The file 'similarity.pkl.gz' was not found.")
    similarity = []

# Load the movies list from compressed file
try:
    with gzip.open('movies (1).pkl.gz', 'rb') as f:
        movies_data = pickle.load(f)

    # Check if movies_data is a DataFrame
    if isinstance(movies_data, pd.DataFrame):
        # Ensure that 'title' column exists
        if 'title' in movies_data.columns:
            movies_list = movies_data['title'].values
        else:
            st.error("The DataFrame does not contain a 'title' column.")
            movies_list = []
    elif isinstance(movies_data, dict):
        # Check if it's a dictionary with 'title' key
        if 'title' in movies_data:
            movies_list = movies_data['title'].values
        else:
            st.error("The dictionary does not contain a 'title' key.")
            movies_list = []
    else:
        st.error("Loaded object is not a recognized format.")
        movies_list = []

except FileNotFoundError:
    st.error("The file 'movies (1).pkl.gz' was not found.")
    movies_list = []
except Exception as e:
    st.error(f"An error occurred: {e}")
    movies_list = []

# Set the title of the Streamlit app
st.title('Movie Recommender System')

# Create a select box for movie options
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies_list
)

# Display recommendations when the button is clicked
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for movie in recommendations:
        st.write(movie)
