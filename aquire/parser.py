# pylint: disable=import-error
import pdftotext
import json
import os

files = []
with open('fileurls.json', 'r') as f:
    files = json.loads(f.read())

def is_file(fname):
    return os.path.isfile(fname)

for file in files:
    fileName = file.split('/')[-1].replace('%20', ' ')

    if is_file('json/'+fileName+'.json'):
        continue

    print fileName

    with open("pdf/" + fileName, "rb") as f:
        pdf = pdftotext.PDF(f)

    pages = []

    for page in pdf:
        # print(page)
        pages.append(page)

    with open('json/' + fileName + '.json', 'w') as f:
        f.write(json.dumps(pages))