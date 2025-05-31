import json
import os
import uuid
from faker import Faker
from datetime import datetime

fake = Faker()

# Your Django model identifier (app_label.model_name)
model_name = "xApiProduct.productcategorymodel"
output_file = os.path.join(os.path.dirname(__file__), 'category.json')

# Generate data
fixture_data = []

for i in range(1, 51):  # Generate 20 categories
    cate_name = fake.unique.word().capitalize() + " Category"
    cate_desc = fake.sentence(nb_words=10)
    uid = uuid.uuid4().hex[:32].lower()
    slug = cate_name.lower().replace(" ", "-")
    
    fixture_data.append({
        "model": model_name,
        "pk": i,
        "fields": {
            "cate_name": cate_name,
            "slug": slug,
            "cate_desc": cate_desc,
            "author": 1001,   
            "uid": uid,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
    })

# Write to JSON file
with open(output_file, 'w') as f:
    json.dump(fixture_data, f, indent=4)

print(f"✅ Generated {len(fixture_data)} category fixtures at: {output_file}")
