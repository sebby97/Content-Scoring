import os
import sys
import json
indir = './'+sys.argv[1]
for root, dirs, filenames in os.walk(indir):
    print('root hi hi hi')
    print(root)
    print('root bye bye bye')
    for r in root:
        for d in dirs:
            print(d)
            for f in filenames:
                if f == '.DS_Store':
                    continue
                filePath = indir+'/'+r+'/'+dirs+'/'+f
                data = json.load(open(filePath))
                with open(filePath, 'w') as outputFile:
                    json.dump(data, outputFile,indent = 4)
