import json
import os
import uuid
from faker import Faker
from datetime import datetime

fake = Faker()

model_name = "xApiProduct.productmetatagmodel"
output_file = os.path.join(os.path.dirname(__file__), 'meta_tags.json')

fixture_data = []

for i in range(1, 51):  # Create 50 meta tags
    tag = fake.unique.word().capitalize() + "Tag"
    meta_title = fake.sentence(nb_words=4)
    meta_desc = fake.sentence(nb_words=10)
    meta_keywords = ", ".join(fake.words(nb=5))
    meta_robot = fake.boolean()
    is_indexed = fake.boolean()
    uid = uuid.uuid4().hex[:32].lower()

    fixture_data.append({
        "model": model_name,
        "pk": i,
        "fields": {
            "tag": tag,
            "meta_title": meta_title,
            "meta_desc": meta_desc,
            "meta_keywds": meta_keywords,
            "meta_robot": meta_robot,
            "is_indexed": is_indexed,
            "author": 1001,
            "uid": uid,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
    })

# Write to file
with open(output_file, 'w') as f:
    json.dump(fixture_data, f, indent=4)

print(f"✅ Generated {len(fixture_data)} product meta tag fixtures at: {output_file}")
