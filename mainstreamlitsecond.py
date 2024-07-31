import streamlit as st
import requests
from PIL import Image
import io
import base64

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"}

def text_to_image(prompt):
    try:
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        return image, None
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {str(e)}\nResponse content: {e.response.content if e.response else 'No response content'}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

st.title("Text to Image Generator")

prompt_input = st.text_area("Enter your prompt", placeholder="Type your text here...")
submit_button = st.button("Generate Image")

if submit_button:
    if not prompt_input.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            image, error = text_to_image(prompt_input)
            if error:
                st.error(error)
            else:
                st.image(image, caption="Generated Image", use_column_width=True)

# Display API token input in the sidebar
api_token = st.sidebar.text_input("Enter your Hugging Face API token", type="password")
if api_token:
    HEADERS["Authorization"] = f"Bearer {api_token}"