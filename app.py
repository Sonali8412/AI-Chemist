### Health Management APP
import os
from dotenv import load_dotenv

# Load all the environment variables
load_dotenv()

# Debugging statement to check if the environment variable is loaded
print(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")

import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

### Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(prompt, image, user_input):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image[0], user_input])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize our streamlit app
input_prompt= """
You are an expert pharmaceutical/Chemist where you need to see the tablets from the image 
and, also provide the details of every drug/tablets items with below format

1. Examine the image carefully and identify the tablets depicted.
2. Describe the uses and functionalities of each tablet shown in the image.
3. Provide information on the intended purposes, features, and typical applications of the tablets.
4. If possible, include any notable specifications or distinguishing characteristics of each tablet.
5. Ensure clarity and conciseness in your descriptions, focusing on key details and distinguishing fa

----
"""

## Initialize our streamlit app
st.set_page_config(page_title="AI Chemist App")

st.header("AI Chemist App")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

submit = st.button("Tell me")
## If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    
    st.subheader("The Response is")
    st.write(response)