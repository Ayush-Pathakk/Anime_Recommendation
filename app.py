import streamlit as st
import pandas as pd
import pickle
from difflib import get_close_matches

st.set_page_config(page_title="Anime Recommendation System", layout="centered")

st.title("🎌 Anime Recommendation System")
st.markdown("Get anime recommendations based on your favorite show!")

@st.cache_data
def load_data():
    anime = pd.read_csv("anime.csv")
    return anime

@st.cache_resource
def load_model():
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return similarity

anime_data = load_data()
similarity = load_model()

def recommend(anime):
    from difflib import get_close_matches
    
    closest_matches = get_close_matches(anime, anime_data['name'], n=1, cutoff=0.6)
    if not closest_matches:
        return ["Anime not found, please check spelling."]
    
    anime = closest_matches[0]
    index = anime_data[anime_data['name'] == anime].index[0]
    distances = similarity[index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = [anime_data.iloc[i[0]]['name'] for i in anime_list]
    return recommendations

anime_list = anime_data['name'].dropna().unique()
selected_anime = st.selectbox("🎯 Choose an anime you like:", anime_list)

if st.button("🔍 Show Recommendations"):
    with st.spinner("Finding the best recommendations..."):
        recommended_anime = recommend(selected_anime)
        if recommended_anime:
            st.subheader("💡 You might also like:")
            for idx, name in enumerate(recommended_anime, start=1):
                st.write(f"{idx}. {name}")
