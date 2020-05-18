import requests
import json
import os.path

with open('fileurls.json') as f:
    fileurls = json.loads(f.read())

def is_file(fname):
    return os.path.isfile('pdf/'+fname)

downloadable = []
def writeFile(url, dest):
    r = requests.get(url, verify=False)
    with open(dest, 'wb') as f:
        f.write(r.content)

for fileurl in fileurls:
    # print fileurl
    filename = fileurl.split('/')[-1]
    # print filename
    if not is_file(filename):
        print 'downloading', fileurl
        # writeFile(fileurl, filename)
        downloadable.append('wget ' + fileurl)
        print 'done.'

with open('exec.sh', 'w') as f:
    f.write('\n'.join(downloadable))