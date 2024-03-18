from flask import Flask, request, jsonify, render_template
import numpy as np
import keras
from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import joblib

app = Flask(__name__)

# Load tokenizer
tokenizer = joblib.load("artifacts/tokenizer.joblib")

# Load model
model = tf.keras.models.load_model("artifacts/next_word_prediction_model.h5")

def generate_next_word(text, model, tokenizer, maxlen=19, padding='pre', wait_time=0.2, num_predictions=5):
    for i in range(num_predictions):
        token_text = tokenizer.texts_to_sequences([text])[0]
        padded_text = pad_sequences([token_text], maxlen=maxlen, padding=padding)
        predict = np.argmax(model.predict(padded_text))
        for word, index in tokenizer.word_index.items():
            if index == predict:
                text = text + " " + word
                print(text)
        time.sleep(wait_time)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    generate_next_word(text, model, tokenizer)
    return render_template('result.html', prediction='Prediction printed in console')

if __name__ == '__main__':
    app.run(debug=True)