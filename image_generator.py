from openai import OpenAI
import config
from PIL import Image
import requests
from io import BytesIO

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_images(keyword, num_images=3, style='on-brand'):  # Customize style
    images = []
    for i in range(num_images):
        prompt = f"Create a {style} image for article on '{keyword}' in {config.NICHE}."
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        img_url = response.data[0].url
        img_response = requests.get(img_url)
        img = Image.open(BytesIO(img_response.content))
        img_path = f"static/images/{keyword.replace(' ', '_')}_{i}.png"
        img.save(img_path)
        images.append(img_path)
    return images