import requests

API_URL = "http://127.0.0.1:8000/api/v1/product-image/"
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTYwNjAzLCJpYXQiOjE3NDgzNjg2MDMsImp0aSI6IjFmYzI4ODJkNzVhZDQ4MzA5ZTIwY2Q1ZjZkNjQ5MzU2IiwidXNlcl9pZCI6MTAwMX0.UIZY4eIlMTBzcmnBKp1Qqy3wtFS97wUAicyZplsB3oM"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def get_all_image_ids():
    image_ids = []
    url = API_URL
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch images: {response.status_code} {response.text}")
            break
        
        data = response.json()
        # Adjust depending on your pagination keys
        results = data.get('results', data)  # if paginated, 'results' usually holds the list
        for img in results:
            image_ids.append(img['id'])
        
        # Pagination: get next page URL if available
        url = data.get('next')
    
    return image_ids

def delete_image(image_id):
    delete_url = f"{API_URL}{image_id}/"
    response = requests.delete(delete_url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Deleted image with ID {image_id}")
    else:
        print(f"Failed to delete image {image_id}: {response.status_code} {response.text}")

def main():
    print("Fetching all product image IDs...")
    image_ids = get_all_image_ids()
    print(f"Found {len(image_ids)} images.")
    
    for img_id in image_ids:
        delete_image(img_id)

if __name__ == "__main__":
    main()
