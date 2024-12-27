from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input_prompt , image , input):
    response = model.generate_content([input_prompt , image, input])
    return response.text

#Streamlit Setup
st.set_page_config(page_title = "Multilanguage Image Extractor")
st.header("Gemini Apllixation")
input = st.text_input("Input Prompt" , key = 'input')#Ask the question
upload_file = st.file_uploader("Choose Image ..." , type= ['jpg' , 'png' , 'jpeg'])#To upload image

#To setup image 
def input_image_details(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_parts = [
            {
                "mimi_type":upload_file.type,
                "data" : bytes_data
            }
        ]
        return image
    else:
        raise FileNotFoundError("No file founded")


#Opening the Image and Final Submitting Button
image = ""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image , caption = "Uploaded Image" , use_column_width = True)
submit = st.button("Tell me about the Image")

input_prompt = "You are an expert in understanding the invoice image and extracting the information from the image and displaying it"

#If submit button is clicked
if submit:
    image_data = input_image_details(upload_file)
    response = get_gemini_response(input_prompt, image_data , input)
    st.subheader("The response is ..")
    st.write(response)
