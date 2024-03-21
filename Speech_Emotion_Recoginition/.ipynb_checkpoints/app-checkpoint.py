import os
import librosa
import numpy as np
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, jsonify

# Load the trained model
model = load_model('artifacts/lstm_model.keras')

# Function to extract features from audio file
def extract_feature(file_path):
    audio_data, sr = librosa.load(file_path)
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr)
    return mfccs

# Function to preprocess features
def preprocess_features(features, max_pad_len=100):
    # Pad or truncate the array to ensure fixed length
    if features.shape[1] < max_pad_len:
        padded_features = np.pad(features, ((0, 0), (0, max_pad_len - features.shape[1])), mode='constant')
    else:
        padded_features = features[:, :max_pad_len]
    return padded_features

# Function to predict emotion
def predict_emotion(file_path):
    # Define emotion labels
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'ps', 'sad']
    
    # Extract features
    features = extract_feature(file_path)
    # Preprocess features
    padded_features = preprocess_features(features)
    # Reshape features to match model input shape
    reshaped_features = np.expand_dims(padded_features, axis=0)  # Add batch dimension
    # Perform prediction
    predicted_emotion = model.predict(reshaped_features)
    # Get the index of the maximum probability
    predicted_class_index = np.argmax(predicted_emotion, axis=1)[0]
    # Get the corresponding emotion label
    predicted_emotion_label = emotion_labels[predicted_class_index]
    return predicted_emotion_label

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index.html')  # Route for index.html
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    audio_file = request.files['file']
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    # Save the uploaded file
    file_path = audio_file.filename
    audio_file.save(file_path)

    # Make prediction
    predicted_emotion = predict_emotion(file_path)

    # Remove the uploaded file
    os.remove(file_path)

    return jsonify({'predicted_emotion': predicted_emotion})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)