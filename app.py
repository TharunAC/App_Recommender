
import streamlit as st
import pandas as pd
import pickle
import requests
from PIL import Image
from io import BytesIO

def is_valid_image(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
            img = Image.open(BytesIO(response.content))
            img.verify()  # Verify that it is, in fact, an image
            return True
    except (requests.RequestException, IOError):
        pass
    return False

def recommend(selected_app,apps_list):
    app_index=apps_list[apps_list['App Name']==selected_app].index[0]
    distances=similarity[app_index]
    recommend_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:21]
    recommend_names=[]
    recommend_icons=[]
    for i in recommend_list:
        icon_url = apps_list.iloc[i[0]]['Icon URL']
        if is_valid_image(icon_url):
            recommend_names.append(apps_list.iloc[i[0]]['App Name'])
            recommend_icons.append(icon_url)
    return recommend_names,recommend_icons

apps_list=pickle.load(open('f1.pkl', 'rb'))
apps_list=pd.DataFrame(apps_list)

similarity = pickle.load(open('app_similarity.pkl', 'rb'))
#recommend("Healthy Benefits+")
selected_app = st.selectbox(
    "Select a app to get recommendations:",
    apps_list['App Name'].values
)
if st.button("Recommedations"):
    names, posters = recommend(selected_app,apps_list)
    num_cols = 5  # Number of columns for movie recommendations

    num_movies = 5  # Total number of movie recommendations

    # Calculate number of rows needed to display all movie recommendations
    num_rows = (num_movies + num_cols - 1) // num_cols

    col1, col2, col3, col4, col5 = st.columns(num_cols)

    index = 0  # Initialize index to track movie recommendations
    for row in range(num_rows):
        # Display movie recommendations in each column
        if index < num_movies:
            col1.markdown(names[index])
            col1.image(posters[index], use_column_width=True)
            index += 1
        if index < num_movies:
            col2.markdown(names[index])
            col2.image(posters[index], use_column_width=True)
            index += 1
        if index < num_movies:
            col3.markdown(names[index])
            col3.image(posters[index], use_column_width=True)
            index += 1
        if index < num_movies:
            col4.markdown(names[index])
            col4.image(posters[index], use_column_width=True)
            index += 1
        if index < num_movies:
            col5.markdown(names[index])
            col5.image(posters[index], use_column_width=True)
            index += 1
