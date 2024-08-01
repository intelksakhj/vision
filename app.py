import streamlit as st
import requests
import io
from PIL import Image
from google.cloud import vision
from google.cloud import translate_v2 as translate
import os

# Set up Google Cloud credentials
# Make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# or use st.secrets for Streamlit Cloud deployment

# Initialize Google Cloud clients
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

def detect_text(image):
    image = vision.Image(content=image)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ''

def translate_text(text, target_language='en'):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

st.title("Image Text Translator")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

target_language = st.selectbox(
    "Select target language",
    ["English", "French", "Spanish", "German", "Italian", "Portuguese", "Russian", "Japanese", "Korean", "Chinese (Simplified)"],
)

language_code = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN",
}

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    if st.button('Translate'):
        with st.spinner('Processing...'):
            # Prepare the image for the Vision API
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Detect text
            detected_text = detect_text(img_byte_arr)
            st.subheader("Detected Text:")
            st.write(detected_text)

            # Translate text
            translated_text = translate_text(detected_text, language_code[target_language])
            st.subheader(f"Translated Text ({target_language}):")
            st.write(translated_text)

st.markdown("---")
st.write("This app uses Google Cloud Vision API for OCR and Google Cloud Translation API for translation.")