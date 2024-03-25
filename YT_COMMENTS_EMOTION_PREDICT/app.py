import torch
import streamlit as st
import transformers
from transformers import pipeline , AutoTokenizer , AutoModelForSequenceClassification
from googleapiclient.discovery import build
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

# Set up YouTube API key
API_KEY = os.getenv("YOUTUBE_API_KEY")  # CREATE .env FILE PUT YOUR YOUTUBE_API_KEY IN THIS FOLDER YOUTUBE_API_KEY = "YOUR ID"

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

model_link = "https://huggingface.co/SamLowe/roberta-base-go_emotions"
# Load model directly
tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")

# Function to check model's maximum input length
def get_max_length():
  return tokenizer.model_max_length

# Function to truncate comments (optional)
def truncate_comment(comment, max_length):
  if len(comment) > max_length:
    comment = comment[:max_length]  # Truncate comment to max_length
  return comment

# Function to extract comments from a YouTube video
def extract_comments(video_id):
  comments = []
  nextPageToken = None

  while True:
    # Make API request to retrieve comments
    response = youtube.commentThreads().list(
      part='snippet',
      videoId=video_id,
      maxResults=100,
      pageToken=nextPageToken
    ).execute()

    # Extract comments from response
    for item in response['items']:
      comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
      comments.append(comment)

    # Check if there are more comments
    nextPageToken = response.get('nextPageToken')
    if not nextPageToken:
      break

  return comments

# Function to analyze video comments
def analyze_video_comments(video_id):
  # Extract comments from YouTube video
  comments = extract_comments(video_id)

  # Get model's maximum input length
  max_length = get_max_length()

  # Analyze emotions for each comment
  emotion_counts = {'joy': 0, 'sadness': 0, 'anger': 0, 'fear': 0, 'surprise': 0, 'love': 0}
  for comment in comments:
    # Truncate comment if necessary (optional)
    comment = truncate_comment(comment, max_length)

    # Perform tokenization
    inputs = tokenizer(comment, return_tensors="pt", truncation=True, padding=True)

    # Forward pass through the model
    outputs = model(**inputs)
    predicted_emotion_index = outputs.logits.argmax().item()
    predicted_emotion = model.config.id2label[predicted_emotion_index]

    # Increment count for the detected emotion
    if predicted_emotion in emotion_counts:
      emotion_counts[predicted_emotion] += 1
    else:
      emotion_counts[predicted_emotion] = 1

  # Calculate emotion percentages
  total_comments = len(comments)
  emotion_percentages = {emotion: (count / total_comments) * 100 for emotion, count in emotion_counts.items()}

  return emotion_percentages

# Home Page
def home():
    st.title("YouTube Emotion Analyzer: Unveiling Sentiments in Comments")
    st.write("This app allows you to predict emotions from YouTube video comments.")
    st.image("https://wpvip.edutopia.org/wp-content/uploads/2023/09/feature_identify-emotions-feelings_all-grades_illustration_JakeOlimb_getty_1395986778.jpg?resize=2000,1125&quality=85" , use_column_width=True)

# Prediction Page
def prediction():
    
    st.image("https://peopledevelopmentmagazine.com/wp-content/uploads/2017/04/Depositphotos_258843620_S-978x620.jpg.webp", use_column_width=True)
    st.title("Youtube Video Comments Emotion Detection")
    st.write("Please enter the YouTube video ID to analyze comments.")
    video_id = st.text_input("Enter YouTube Video ID: ")
    st.write("Example Video Link : https://www.youtube.com/watch?v=HfczE4zrOTU")
    st.write("Example Video Id : HfczE4zrOTU")

    
    if st.button("Predict Emotions"):
        if video_id:
            try:
                # Analyze emotions for the video comments
                emotion_percentages = analyze_video_comments(video_id)
                st.write(f"VIDEO LINK : https://www.youtube.com/watch?v={video_id}")
                st.write("YOU ENTERED VIDEO ID:", video_id) 
                st.title("Emotion Percentages:")
                for emotion, percentage in emotion_percentages.items():
                    st.write(f"{emotion}: {percentage:.2f}%")

                # Display top 5 comments
                comments = extract_comments(video_id)[:5]
                st.title("Top 5 Comments:")
                for comment in comments:
                    st.write(comment)

            except:
                st.write("Error: Invalid YouTube Video ID.")



# App
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "Prediction"))
    
    if page == "Home":
        home()
    elif page == "Prediction":
        prediction()

if __name__ == "__main__":
    main()