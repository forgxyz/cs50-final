#!python
"""Generate csv of user input categories with corresponding IDs"""
import csv

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

with open('category_ids.csv', 'w', newline='') as f:
    fieldnames = ['CategoryID', 'Category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in cat_ids.items():
        writer.writerow({'CategoryID' : key, 'Category' : value})

print(cat_ids)