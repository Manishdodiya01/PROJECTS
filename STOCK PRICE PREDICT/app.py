import streamlit as st
import numpy as np
import pickle
import joblib

model = joblib.load('artifacts/stock_model.joblib')

image = "6688.jpg_860.jpg"
header_style = """
    background-color: #000000; /* Black */
    padding: 20px;
    border-radius: 10px;
"""

subheader_style = """
    background-color: #1C1C1C; /* Dark Gray */
    padding: 10px;
    border-radius: 5px;
"""


st.set_page_config(page_title="Stock Price Predicion App" , layout='wide')
st.title('Stock Price Predicion App')


# SIDE BAR FOR USER INPUT
st.sidebar.header('User Input Parameters')

open_price = st.sidebar.number_input('Open Price',min_value=0.0)
high_price = st.sidebar.number_input('High Price',min_value=0.0)
low_price = st.sidebar.number_input('Low Price',min_value=0.0)
volume = st.sidebar.number_input('Volume',min_value=0.0)

user_input = np.array([[open_price, high_price, low_price, volume]])

prediction = model.predict(user_input)

st.subheader('Stock Price Prediction')
st.write(f"Predicted Close Price: {prediction[0]:.2f}")


st.image(image , caption='' , use_column_width=True)

