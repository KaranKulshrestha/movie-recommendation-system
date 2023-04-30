import pickle
import pandas as pd
import streamlit as st
import requests

st.title("Movie Recommendation Engine")

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

option = st.selectbox("Find the best movies for you", movies['title'].values)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetchPoster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=638394f79178dc5824fe68779be5777b&language=en-US".format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        #fetch poster from api
        recommend_movies.append(movies.iloc[i[0]]['title'])
        recommend_movies_posters.append(fetchPoster(movie_id))
    return recommend_movies, recommend_movies_posters

if st.button('Recommend'):
    names, posters = recommend(option)
    col1, col2, col3, col4,  col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])