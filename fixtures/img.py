import os
import requests

IMAGE_DIR = "media/products"
os.makedirs(IMAGE_DIR, exist_ok=True)

for i in range(1, 501):
    url = f"https://picsum.photos/seed/product{i}/400/400"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            image_path = os.path.join(IMAGE_DIR, f"product_{i}.jpg")
            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"[{i}/500] Downloaded: {image_path}")
        else:
            print(f"[{i}] Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"[{i}] Error: {str(e)}")
