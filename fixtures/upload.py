import os
import requests

# API endpoint URL
API_URL = "http://127.0.0.1:8000/api/v1/product-image/"

# Directory where your images are stored
MEDIA_DIR = "/home/falcon/servers/xApi/xApi/fixtures/media/products"

# Your token for authentication — replace with your actual token string
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTYwNjAzLCJpYXQiOjE3NDgzNjg2MDMsImp0aSI6IjFmYzI4ODJkNzVhZDQ4MzA5ZTIwY2Q1ZjZkNjQ5MzU2IiwidXNlcl9pZCI6MTAwMX0.UIZY4eIlMTBzcmnBKp1Qqy3wtFS97wUAicyZplsB3oM"

HEADERS = {
    # "Authorization": f"Token {API_TOKEN}"
    # Use "Bearer" if your API expects Bearer tokens:
    "Authorization": f"Bearer {API_TOKEN}"
}

def upload_product_image(product_id, image_path):
    with open(image_path, 'rb') as img_file:
        files = {
            'product_image': (os.path.basename(image_path), img_file, 'image/jpeg'),
        }
        data = {
            'product': product_id,
            'is_primary': True,
            'alt_text': f"Image for product {product_id}",
            'author': 1001,
        }
        response = requests.post(API_URL, data=data, files=files, headers=HEADERS)
        return response

def main():
    # We assume product IDs are integers from 1 up to max file number you have
    # Alternatively, you can scan the directory and parse numbers from filenames
    # For example, here we scan all product_*.jpg files and extract the number to upload
    
    for filename in os.listdir(MEDIA_DIR):
        if filename.startswith("product_") and filename.endswith(".jpg"):
            # Extract product_id from filename like product_123.jpg
            try:
                product_id = int(filename.split("_")[1].split(".")[0])
            except ValueError:
                print(f"Skipping file with invalid product id: {filename}")
                continue
            
            image_path = os.path.join(MEDIA_DIR, filename)
            response = upload_product_image(product_id, image_path)
            if response.status_code == 201:
                print(f"Uploaded image for product ID {product_id}")
            else:
                print(f"Failed to upload image for product ID {product_id}: {response.status_code} {response.text}")

if __name__ == "__main__":
    main()
