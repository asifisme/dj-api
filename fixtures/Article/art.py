import os 
import json 
import uuid 
import random 
from slugify import slugify  # pip install python-slugify 
from faker import Faker 
from datetime import datetime

fake = Faker() 

model_name = "xApiArticle.articlemodel" 
output_file = os.path.join(os.path.dirname(__file__), 'articles.json') 

fixture_data = [] 


for i in range(1, 501):  # Generate 500 articles
    title = fake.unique.sentence(nb_words=6).rstrip(".")
    slug = slugify(title)
    desc = fake.text(max_nb_chars=300)
    summary = fake.text(max_nb_chars=100)
    read_time = random.randint(1, 10)  # Read time in minutes
    views_count = random.randint(0, 10000)
    
    cate_id = random.randint(1, 50)  # Assuming categories are already created
    meta_tag_ids = random.sample(range(1, 51), random.randint(1, 3))  # Randomly select 1-3 meta tags
    
    uid = uuid.uuid4().hex[:32].lower()
    
    fixture_data.append({
        "model": model_name,
        "pk": i,
        "fields": {
            "author": 1001,  # Assuming author ID is 1001
            "cate_id": cate_id,
            "meta_tag": meta_tag_ids,
            "title": title,
            "slug": slug,
            "desc": desc,
            "summary": summary,
            "read_time": read_time,
            "views_count": views_count,
            "uid": uid,
            "published_at": True if random.random() > 0.5 else False,
            "approve": True if random.random() > 0.2 else False,
            "is_active": True,
            "created": datetime.now().isoformat(), 
            "modified": datetime.now().isoformat()
        }
    })


# Write to JSON file
with open(output_file, 'w') as f:
    json.dump(fixture_data, f, indent=4) 
print(f"✅ Generated {len(fixture_data)} article fixtures at: {output_file}") 