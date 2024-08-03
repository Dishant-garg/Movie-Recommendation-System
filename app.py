import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=95d0bb143d7b294c235aa6dd199e2c47&language=en-US%27'.format(movie_id))
  data = response.json()
  return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
  
  recommend_movies = []
  recommended_movies_posters =[]
  for i in movies_list:
    movies_id = movies.iloc[i[0]].movie_id
    recommend_movies.append(movies.iloc[i[0]].title)
    recommended_movies_posters.append(fetch_poster(movies_id))
  return recommend_movies,recommended_movies_posters
movies = pd.DataFrame(movie_dict)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Movies List',
movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
   