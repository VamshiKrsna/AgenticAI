# helper for summarizing images using gemini api

from google.generativeai import GenerativeModel
import google.generativeai as genai
from PIL import Image

def setup_gemini_api(API_KEY:str)->GenerativeModel:
    genai.configure(api_key = API_KEY)
    model = GenerativeModel('gemini-1.5-flash')
    return model

def summarize_image(img_object:str,model:GenerativeModel)->str:
    try:
        image = Image.open(img_object)
        response = model.generate_content([
            "Summarize this image in 2-3 lines.",
            image
        ])
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

