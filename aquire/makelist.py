import json

with open('fileurls.json') as f:
    fileurls = json.loads(f.read())

downloadable = []

for fileurl in fileurls:
    # print fileurl
    filename = fileurl.split('/')[-1]
    # print filename
    if 'DEMOCRAT' in filename:
        print 'sortable', filename
        # writeFile(fileurl, filename)
        downloadable.append('python sorter.py ' + filename + '.json > ' + filename + '.txt')
        print 'done.'


with open('sort.bat', 'w') as f:
    f.write('\n'.join(downloadable))