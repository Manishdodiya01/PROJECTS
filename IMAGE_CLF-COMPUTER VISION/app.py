import streamlit as st
import tensorflow as tf
import keras
import numpy as np
from PIL import Image

#  This can be a useful optimization to avoid loading the model every time the function is called
# improving the performance of your Streamlit app.

@st.cache(allow_output_mutation=True) # INCREASE SPEED
def load_model():
 model = keras.models.load_model('flower_model_trained.hdf5')    
 return model

def predict_class(image , label):
 image = tf.cast(image , tf.float32)
 image = tf.image.resize(image , (180,180))
 image = np.expand_dims(image , axis=0)
 
 prediction = model.predict(image)

 return prediction


model = load_model()

st.info('UPLOAD THIS TYPE OF IMAGE')

i = ['data/daisy.jpg', 'data/dandelion.jpg', 'data/rose.jpg' , 'data/sunflower.jpg' , 'data/tulips.jpg']
st.image(i , width=200)


AUDIO = 'data/chipi-chipi-chapa-chapa.mp3'
AUDIO_2 = 'data/erro.mp3'

st.title('PLAY THE MUSIC AND DO WHATEVER YOU WANT MEN')
st.audio(AUDIO)


FILE = st.file_uploader(label="YOU ARE IN RIGHT PLACE 🫂" , type=['png' , 'jpg'])
button = st.button('GO FOR GOAL')

if FILE is None:
 st.text('WHAT A DOG DO MEN 😶🐕')  # KAI PAN UPLOAD NA KRYU HOY TYARE 👍


else:
 

 slot = st.empty()
 slot.text('WAIT FOR THE 💣') 

 text_image = Image.open(FILE)

 st.image(text_image , caption='LOADED IMAGE' , width=180)

 pred = predict_class(text_image , model)


 class_names = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

 result = class_names[np.argmax(pred)]

 output = "THE IMAGE IS A " + result

 slot.text('HEY MAN ARE YOU HAPPY 👍')

 st.success(output)
 st.text('YOU GOT SUCCESS PLAY THE SONG')
 st.audio(AUDIO)

 st.info('GO TO HELL 🫂')



