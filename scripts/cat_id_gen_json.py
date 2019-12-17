#!python
"""Generate csv of user input categories with corresponding IDs"""
import json

cats = []

while True:
    addition = input("Enter a category: ")
    if addition == 'q':
        break
    cats.append(addition.title())

cats.sort()

cat_ids = {}

for count, item in enumerate(cats):
    cat_ids[count] = item

with open('category_ids.json', 'w+') as f:
    json.dump(cat_ids, f)

print(cat_ids)
