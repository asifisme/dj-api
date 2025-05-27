import json
import os
import uuid
import random
from faker import Faker
from datetime import datetime
from slugify import slugify  # pip install python-slugify

fake = Faker()

model_name = "xApiProduct.productmodel"
output_file = os.path.join(os.path.dirname(__file__), 'products.json')

fixture_data = []

for i in range(1, 501):  # Generate 500 products
    title = fake.unique.sentence(nb_words=3).rstrip(".")
    name = title
    slug = slugify(title)
    description = fake.text(max_nb_chars=200)
    
    price = round(random.uniform(10.0, 1000.0), 2)
    discount_percent = round(random.uniform(0, 50), 2)
    weight = round(random.uniform(0.1, 10.0), 2)
    stock = random.randint(10, 500)
    min_order_quantity = random.randint(1, 5)

    warranty_info = fake.sentence(nb_words=5)
    shipping_info = fake.sentence(nb_words=5)
    return_policy = fake.sentence(nb_words=5)

    sku = fake.unique.bothify(text='SKU-#####-????')
    unq_num = str(uuid.uuid4().int % 10000000000000000000)
    uid = uuid.uuid4().hex[:32].lower()
    pro_uuid = str(uuid.uuid4())

    meta_tag_ids = random.sample(range(1, 51), random.randint(1, 3))
    category_id = random.randint(1, 50)

    fixture_data.append({
        "model": model_name,
        "pk": i,
        "fields": {
            "category": category_id,
            "author": 1001,
            "meta_tag": meta_tag_ids,
            "name": name,
            "title": title,
            "slug": slug,
            "description": description,
            "weight": weight,
            "sku": sku,
            "price": price,
            "discount_percent": discount_percent,
            "stock": stock,
            "warranty_information": warranty_info,
            "shipping_information": shipping_info,
            "return_policy": return_policy,
            "min_order_quantity": min_order_quantity,
            "unq_num": unq_num,
            "pro_uuid": pro_uuid,
            "is_available": True,
            "is_approved": True,
            "rating": 0,
            "views_count": 0,
            "sold_count": 0,
            "uid": uid,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
    })

# Write JSON file
with open(output_file, 'w') as f:
    json.dump(fixture_data, f, indent=4)

print(f"✅ Successfully generated {len(fixture_data)} product fixtures at: {output_file}")
