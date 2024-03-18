from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
import time
import joblib
import nltk
from keras.models import Sequential
from keras.layers import LSTM , Dense , Embedding , BatchNormalization , GRU , Dropout
from keras.callbacks import EarlyStopping
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
nltk.download('punkt')

app = Flask(__name__)

# Load tokenizer
tokenizer = joblib.load("artifacts/tokenizer.joblib")

# Load model
model = tf.keras.models.load_model("artifacts/next_word_prediction_model.h5")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    num_predictions = 10
    maxlen = 19
    padding = 'pre'
    wait_time = 0.2
    predicted_texts = []

    for i in range(num_predictions):
        token_text = tokenizer.texts_to_sequences([text])[0]
        padded_text = pad_sequences([token_text], maxlen=maxlen, padding=padding)
        predict = np.argmax(model.predict(padded_text))
        predicted_word = None
        for word, index in tokenizer.word_index.items():
            if index == predict:
                text = text + " " + word
                predicted_word = word
        predicted_texts.append(text)
        time.sleep(wait_time)

    return render_template('result.html', predicted_texts=predicted_texts)



if __name__ == '__main__':
    app.run(debug=True)