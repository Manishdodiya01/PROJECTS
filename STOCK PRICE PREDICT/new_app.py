import streamlit as st
import numpy as np
import pickle
import joblib


model = joblib.load('stock_model.joblib')
photo_path = "data/6688.jpg_860.jpg"

st.set_page_config(page_title='My Streamlit App' , layout='wide')

def home_page():
    st.subheader('🫂')
    st.write('Welcome To Stock Prediction Web 💣')
    

    st.image(photo_path , use_column_width=True)

def page_stock_prediction():
    st.title('📈 Stock Price Prediction App')

    # Sidebar for user input
    st.sidebar.header('User Input Parameters')
    open_price = st.sidebar.number_input('Open Price', min_value=0.0)
    high_price = st.sidebar.number_input('High Price', min_value=0.0)
    low_price = st.sidebar.number_input('Low Price', min_value=0.0)
    volume = st.sidebar.number_input('Volume', min_value=0.0)

    user_input = np.array([[open_price, high_price, low_price, volume]])

    # Button to trigger prediction
    if st.button('Predict'):
        prediction = model.predict(user_input)
        st.subheader('Stock Price Prediction')
        st.write(f"Predicted Close Price: {prediction[0]:.2f}")


# page selection
        
pages = {
    "HOME PAGE 💀" : home_page,
    "Stock Prediction 👍" : page_stock_prediction,
}

# SIDEBAR FOR PAGE SELECTION
selected_page = st.sidebar.radio('SELECT PAGE' , list(pages.keys()))

# DISPLAY THE SELECTED PAGE

pages[selected_page]()