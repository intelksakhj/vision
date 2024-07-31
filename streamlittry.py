import streamlit as st
import requests
from PIL import Image
import io

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"}

def text_to_image(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        response.raise_for_status()
        
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        return image, None
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

st.title("Text to Image Generator")

prompt_input = st.text_area("Enter your prompt", placeholder="Type your text here...")
submit_button = st.button("Generate Image")

if submit_button:
    with st.spinner("Generating image..."):
        image, error = text_to_image(prompt_input)
        if error:
            st.error(error)
        else:
            st.image(image, caption="Generated Image", use_column_width=True)
