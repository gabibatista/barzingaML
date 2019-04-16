# # ETL - Extract, Transform and Load of Barzinga data
import pandas as pd
import json

df = pd.read_json('data/barzinga_all_products.json')
df.count()

products = []
for i in df.index:
    product = {
        'id': str(df['id'][i]),
        'description': df['description'][i],
        'label': i
    }
    products.append(product)

with open('data/products_dict.json', 'w') as f:
    json.dump(products, f)
