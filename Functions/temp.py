import json
import sys


file1 = json.load(open(sys.argv[1]+'output/ranks/engagementTotalTime/rank.json'))
file2 = json.load(open(sys.argv[1]+'ranks/engagementTotalTime/ranks.json'))

for key in file1.keys():
    if file1[key]==file2[key]:
        continue
    else:
        print("Difference at key: "+key)
