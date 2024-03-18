import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd 
import numpy as np 
import streamlit as st 
import sklearn 
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = joblib.load("TfidfVectorizer.joblib")
model = joblib.load("BernoulliNB_Model.joblib")



stop_words = set(stopwords.words('english'))


def preprocess(text):

    text = text.lower() # Convert in to lower
    # Combine punctuation removal and specific character removal:
    text = re.sub(r"[^\w\s#@\$]" , " " , text)
    tokens = text.split() # TOKENIZE

    # REMOVE STOP-WORDS
    tokens = [word for word in tokens if word not in stop_words]

    # STEMMING : STEAMMING EXMAPLE CONVERT "LOVING" TO "LOVE" , "DANCING" TO "DANC"

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    return " ".join(tokens)


st.title('Email/SMS Spam Classifier')


input_sms = st.text_input('Enter the message')

if st.button('Predict'):
    # 1.preprocess
    transformed_sms = preprocess(input_sms)
    # 2.vectorize   
    vector_input = tfidf.transform([transformed_sms])
    # 3.predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header('Spam')
    else:
        st.header('Not Spam')