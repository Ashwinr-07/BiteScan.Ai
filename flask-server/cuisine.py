import os
import requests
from PIL import Image
import openai
import base64
import io
from dotenv import load_dotenv


# OpenAI API key from environment variable
## Load Key 
openai.api_key = 'API - Key'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def run_chatgpt(image_path):
    base64_image = encode_image(image_path)
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds the cuisines of food items in images."},
            {"role": "user", "content": [
                {"type": "text", "text": "What is the cuisine of this food? in one word, else return the generic name of the dish"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ],
        temperature=0.0,
    )
    
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    # Provide the path to your image file
    image_path = "image3.png"
    
    print("Starting the food recognition process...")
    # Call the food recognition function
    cuisine = run_chatgpt(image_path)
    
    if cuisine:
        print("Likely Cuisine:", cuisine)
    else:
        print("No cuisine information could be determined.")
