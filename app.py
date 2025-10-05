### AI Chemist App
import os
from dotenv import load_dotenv

# Load all the environment variables
load_dotenv()

import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")

# Fix for API key format: remove quotes if present
if api_key:
    api_key = api_key.strip('\"\'')
    genai.configure(api_key=api_key)
else:
    st.error("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")

### Function to load Google Gemini API And get response
def get_gemini_response(prompt, image, user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if user_input:
        response = model.generate_content([prompt, image[0], user_input])
    else:
        response = model.generate_content([prompt, image[0]])
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

# Responsive layout with columns
col1, col2 = st.columns(2)

with col1:
    user_input = st.text_input("Additional Input (optional): ", key="input")

with col2:
    uploaded_file = st.file_uploader("Choose an image of tablets...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", width=400)  # Use width for responsiveness

submit = st.button("Analyze Tablets")

## If submit button is clicked
if submit:
    if not uploaded_file:
        st.error("Please upload an image of the tablets.")
    elif not api_key:
        st.error("API key not configured. Please set GOOGLE_API_KEY in your .env file.")
    else:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, user_input)
            st.subheader("Analysis Result")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
