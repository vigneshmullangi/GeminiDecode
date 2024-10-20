from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load all environment variables from the .env file
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini model and get responses
def get_gemini_response(image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction")
st.header("GeminiDecode: Multilanguage Document Extraction By Gemini Pro")
text = "Multilanguage Document Extraction by Gemini Pro is a cutting-edge solution designed to extract and process data from documents in multiple languages with unparalleled efficiency. By leveraging advanced natural language processing (NLP) and machine learning algorithms, it seamlessly identifies, extracts, and categorizes information from diverse document formats, ensuring accuracy and speed. Ideal for global businesses, GeminiDecode supports over 50 languages, providing robust data extraction capabilities that streamline workflows, enhance productivity, and improve decision-making processes."
styled_text = f"<span style='font-family: serif; color: #b7b7b7;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert image to RGB mode if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image_path = "uploaded_image.jpg"

    submit = st.button("Tell me about the document")
    if submit:
        try:
            image_data = input_image_details(uploaded_file)
            input_prompt = """
            You are an expert in understanding various types of documents. 
            We will upload an image of a document, and you will have to answer any questions based on the uploaded document image.
            Translate the content of the document to English.
            """
            response = get_gemini_response(image_data, input_prompt)
            st.subheader("The response is:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
