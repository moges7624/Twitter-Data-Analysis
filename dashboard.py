import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt
from wordcloud import WordCloud


data_for_vis = pd.read_csv("./notebooks/cleaned_data.csv")
polarity=[-1, 1]
polarity_text=["Negative", "Positive"]

st.sidebar.header('User Input Values')


def user_input_features():

    Polarity = st.sidebar.selectbox('Select Polarity',polarity, 0)



    # data = {'Polarity': Polarity}
    # features = pd.DataFrame(data, index=[0])
    
    if Polarity == -1:
        return "Negative"
    else: 
        return "Positive"



selected_polarity = user_input_features()


def draw_word_cloud(df):
    # Word-cloud for Positive tweets
    data_pos = df[df['score'] == selected_polarity.lower()]['original_text']
    

    plt.figure(figsize=(20,20))
    wc = WordCloud(max_words=150, width=1600, height=800, collocations=False).generate(" ".join(data_pos))
    plt.imshow(wc)
    st.pyplot()



st.subheader(f'Selected Polarity is {selected_polarity}')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.write(draw_word_cloud(data_for_vis))
# st.pyplot(draw_word_cloud(data_for_vis))