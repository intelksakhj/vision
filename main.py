import gradio as gr
import requests
from PIL import Image
import io

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"}

def text_to_image(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        return image, None  # Return the image and no error message
    except requests.exceptions.RequestException as e:
        error_message = f"API request failed: {str(e)}"
        print(error_message)  # Log the error
        return None, error_message  # Return no image and the error message
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)  # Log the error
        return None, error_message  # Return no image and the error message

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Text to Image Generator</h1>")
    
    with gr.Row():
        with gr.Column():
            prompt_input = gr.Textbox(label="Enter your prompt", placeholder="Type your text here...", lines=3)
            submit_button = gr.Button("Generate Image")
        
        with gr.Column():
            output_image = gr.Image(label="Generated Image")
            error_output = gr.Textbox(label="Error Message", visible=False)
    
    def process_request(prompt):
        image, error = text_to_image(prompt)
        if error:
            return None, error, gr.update(visible=True)
        return image, None, gr.update(visible=False)
    
    submit_button.click(
        process_request, 
        inputs=prompt_input, 
        outputs=[output_image, error_output, error_output]
    )

# Launch the app
demo.launch()