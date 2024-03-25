# YouTube Video Emotion Analyzer

## Introduction
This project is a YouTube video emotion analyzer built using Streamlit and Hugging Face's transformers library. It analyzes the emotions expressed in the comments of a YouTube video using the SamLowe/roberta-base-go_emotions model.

## Libraries Used
- torch
- streamlit
- transformers
- googleapiclient
- dotenv

## Installation
To run this project locally, make sure you have Python installed on your system. You can install the required dependencies using pip:

```bash
pip install torch streamlit transformers google-api-python-client python-dotenv


##  Create a .env file in the root directory and add your YouTube API key in the following format:

- YOUTUBE_API_KEY=your_api_key_here

## Run the Streamlit app using the following command:

- streamlit run app.py

## Credits

-This project uses the SamLowe/roberta-base-go_emotions model from Hugging Face's model hub.


## Make sure to replace `your_api_key_here` with your actual YouTube API key in the `.env` file. Also, feel free to add more detailed instructions or descriptions as needed.

