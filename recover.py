import json
from pathlib import Path

pathlist = list(Path('splits/').glob('**/*.json'))
if not pathlist:
    print('No parts were found, shutting down...')
    exit()
files_len = len(pathlist)
k = 0
with open(pathlist[0], 'r') as json_file:
    k = json.load(json_file)['k']
if files_len < k:
    print('Number of parts is less than needed, shutting down...')
    exit()
# check for parts matches
real_files_len = files_len
for i in range(files_len - 1):
    part1 = 0
    with open(pathlist[i], 'r') as f1:
        part1 = json.load(f1)['part']
    for j in range(i + 1, files_len):
        part2 = 0
        with open(pathlist[j], 'r') as f2:
            part2 = json.load(f2)['part']
        if part1 == part2:
            real_files_len -= 1
            pathlist.pop(j)
            j -= 1
if real_files_len < k:
    print('Number of unique parts is less than needed, shutting down...')
    exit()

print('All parts are found, proceeding to secret recovery.')
parts = []
for i in range(real_files_len):
    with open(pathlist[i], 'r') as f:
        parts.append(json.load(f)['part'])
#print(parts)

secret = 0
for j in range(k):
    prod = 1
    for m in range(k):
        if m != j:
            prod *= (m+1)/(j-m)
    secret += parts[j] * prod

with open('secret.json', 'w') as f:
    data = {}
    data['k'] = k
    data['secret'] = secret
    json.dump(data, f, indent = 4)

