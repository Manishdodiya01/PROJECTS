import joblib
import nltk
import streamlit as st
import sklearn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


model = joblib.load('lr_model_without_hyper-tunning')
tf_idf = joblib.load('tf_idf.joblib')

stop_words = set(stopwords.words('english'))
steamer = PorterStemmer()

def preprocess_text(text):

    text = text.lower()
    text = re.sub(r"[#@$]" , " " , text)
    text = re.sub("[^\w\s]" , " " , text) # combine punctuation
    text = word_tokenize(text) # Tokenize # simple word split
    text = [word for word in text if word not in stop_words] # remove stopword "the am"
    text = [steamer.stem(i) for i in text]
    return " ".join(text)


# fun to predict emotion
def predict_emotion(text):
    preprocessed_text = preprocess_text(text)
    transformed_text = tf_idf.transform([preprocessed_text])
    prediction = model.predict(transformed_text)[0]
    return prediction


# header
st.title('Emotion Analysis')
st.markdown('### Analysis the emotion of your Text')

# sidebar
st.sidebar.title('Input Text')
user_input_text = st.sidebar.text_input('Enter Text')

# prediction
if st.sidebar.button('Predict'):
    if user_input_text:
        predicted_emotion = predict_emotion(user_input_text)
        if predicted_emotion == 0:
            st.write('Emotion: Joy')
        elif predicted_emotion == 1:
            st.write('Emotion: Fear')
        elif predicted_emotion == 2:
            st.write('Emotion: Anger')
        elif predicted_emotion == 3:
            st.write('Emotion: Sadness')
    else:
        st.warning('Please enter some text to predict emotion.')
