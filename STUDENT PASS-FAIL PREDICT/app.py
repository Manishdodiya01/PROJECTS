import streamlit as st 
import joblib
import numpy as np 
import sklearn


model = joblib.load('artifacts/pass-fail.joblib')

st.title('STUDENT PASS/FAIL PREDICTION')

st.sidebar.header('USER INPUT')


study_hour = st.sidebar.slider('Study Hours', min_value=0.0, max_value=10.0, step=0.1, value=5.0)
previous_exam_score = st.sidebar.slider('Previous Exam Score', min_value=0.0, max_value=100.0, step=1.0, value=50.0)


if st.sidebar.button('Submit'):
    # User input as numpy array
    user_input = np.array([[study_hour, previous_exam_score]])

    # Make prediction
    prediction = model.predict(user_input)

    # Display prediction
    st.subheader('Pass/Fail Prediction')
    if prediction == 0: # why we use prediction[0] beacause this can give result like this [1] we want this 1 / # array([1], dtype=int64) indexing only the one
        st.write('Result: Fail')
    else:
        st.write('Result: Pass')
