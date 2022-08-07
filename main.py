import pandas as pd
import streamlit as st
import numpy as np
import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import main_functions

nltk.download("punkt")
nltk.download("stopwords")

st.title("COP 4814- Web Application Programming")

st.title ("Project 1")

st.subheader("Part A-The Stories API")
st.write("This app uses the Top Stories API to display the most common words used in the "
         "top current articles, based on a specified topic select by the user. The data "
         "is displayed as a line chart and a wordcloud image.")

st.subheader("I - Topic Selection")
name=st.text_input("Please enter your name")

st.write(" ")
st.write(" ")
str1= ""

api_key_dict = main_functions.read_from_file("JSON files/api_key.JSON")
api_key=api_key_dict["my_key"]


options= st.selectbox("Select your topic of interests", [
    "", "arts", "automobiles", "books", "business", "fashion", "food", "health", "home",
    "insider", "magazine", "movies", "nyregions", "obituaries", "opinions", "politics",
    "realestate", "science", "sports", "sundayreview", "technology", "theatre", "t-magazine",
    "travel", "upshot", "us", "world"
])

url = "https://api.nytimes.com/svc/topstories/v2/" + options + ".json?api-key=" + api_key

response = requests.get(url).json()

main_functions.save_to_file(response, "JSON files/response.json")

my_articles = main_functions.read_from_file("JSON files/response.json")

print(type(my_articles))

for i in my_articles["results"]:
    str1= str1 +i["abstract"]



if options:
    st.write ("Hi ", name, ", you selected {}".format(options), ".")
    st.subheader("II - Frequency Distributor")


words = word_tokenize(str1)
fdist= FreqDist(words)

words_no_punc=[]

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

fdist2= FreqDist(words_no_punc)
stopwords=stopwords.words("english")

clean_words=[]

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

print(len(clean_words))

if st.checkbox("Click here to generate frequency distribution."):
    fdist3=FreqDist(clean_words)
    sentences = sent_tokenize(str1)

    if st.checkbox("Click here to display a frequency distribution graph."):
        most_common= pd.DataFrame(fdist3.most_common((10)))
        df= pd.DataFrame({"words": most_common[0], "count":most_common[1]})
        import plotly.express as px

        fig=px.line(df, x="words", y="count", title='')
        st.plotly_chart(fig)
        pprint(fdist3.most_common(10))

wordcloud = WordCloud().generate(str1)
if options:
    st.subheader("III - WordCloud")
    if st.checkbox("Click here to generate wordcloud"):
            fig, ax = plt.subplots()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(fig)

api_key_dict = main_functions.read_from_file("JSON files/api_key.JSON")
api_key=api_key_dict["my_key"]
my_key=api_key

str2= ""

st.subheader("Part B- Most Popular Articles")
st.write("Select if you want to see the most shared, emailed or viewed articles")

action_article = st.selectbox("Select your preferred set of articles", ["", "shared", "emailed", "viewed articles"])
time_frame=st.selectbox("Select the period of time(the last days", ["", "1", "7", "30"])

url2="https://api.nytimes.com/svc/mostpopular/v2/" +action_article + "/" + time_frame + ".json?api-key" + my_key

response = requests.get(url).json()

main_functions.save_to_file(response, "JSON files/response.json")

my_articles2= main_functions.read_from_file("JSON files/response.json")

pprint(my_articles2)
words2 = word_tokenize(str2)
fdist4= FreqDist(words2)

words_no_punc2=[]

for w in words:
    if w.isalpha():
        words_no_punc2.append(w.lower())

fdist5= FreqDist(words_no_punc2)


clean_words2=[]

for w in words_no_punc2:
    if w not in stopwords:
        clean_words2.append(w)

for i in my_articles2["results"]:
    str2= str2 +i["abstract"]
print(type(my_articles))

wordcloud2 = WordCloud().generate(str2)
most_common= pd.DataFrame(fdist5.most_common((10)))
df= pd.DataFrame({"words": most_common[0], "count":most_common[1]})



if action_article and time_frame:
    fig, ax = plt.subplots()
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)