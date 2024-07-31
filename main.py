import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import random

def generate_image_with_text(text, width=512, height=512):
    # Create a new image with a random background color
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Use a default font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text position
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) / 2, (height - text_height) / 2)

    # Draw text on image
    draw.text(position, text, fill=(255, 255, 255), font=font)

    return image

st.title("Text to Image Generator")

prompt_input = st.text_area("Enter your text", placeholder="Type your text here...")
submit_button = st.button("Generate Image")

if submit_button:
    if not prompt_input.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Generating image..."):
            image = generate_image_with_text(prompt_input)
            st.image(image, caption="Generated Image", use_column_width=True)

            # Provide download button
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name="generated_image.png",
                mime="image/png"
            )