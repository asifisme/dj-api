import os 
import json 
import uuid 
from faker import Faker 
from datetime import datetime 

fake = Faker() 
model_name = "xApiArticle.articlecategorymodel" 
output_file = os.path.join(os.path.dirname(__file__), 'category.json') 

# Generate data 
fixture_data = [] 

for i in range(1, 51):  # Generate 50 categories
    cate_name = fake.unique.word().capitalize() + " Category"
    uid = uuid.uuid4().hex[:32].lower()
    
    fixture_data.append({
        "model": model_name,
        "pk": i,
        "fields": {
            "cate_name": cate_name,
            "author": 1001,  # Assuming author ID is 1001
            "uid": uid,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "is_active": True
        }
    })

# Write to JSON file 
with open(output_file, 'w') as f:
    json.dump(fixture_data, f, indent=4)
print(f"✅ Generated {len(fixture_data)} category fixtures at: {output_file}") 