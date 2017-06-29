import json
import sys


def recursiveCheck(output1,output2,path):
    for key in output1.keys():
        if type(output1[key]) == type(dict()):
            if key not in output2:
                print("\n--"+path+'[\''+key+"\']--doesn't exist in Output 2\n")
            else:
                recursiveCheck(output1[key],output2[key],path+'[\''+key+'\']')
                continue

        if key not in output2:
            print("\nKey path --"+path+'[\''+key+"\']-- doesn't exist in input file 2\n")
        elif ((output1[key] != output2[key]) ):#and key!='startingQuantum'):
            if(type(output1[key])==type(list())):
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key][0:10])+'\tFile 2:\t'+str(output2[key][0:10])+'\n')
            else:
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key])+'\tFile 2:\t'+str(output2[key])+'\n')


scoringprofile = json.load(open('./'+sys.argv[1]+'/scoringprofile.json'))
groups = scoringprofile['groups']

for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:

            output1 = json.load(open(sys.argv[1]+'/scores/engagementTimeSeries/'+profile+'.json'))
            output2 = json.load(open(sys.argv[1]+'output/scores/engagementTimeSeries/'+profile+'.json'))

            recursiveCheck(output1,output2,'')
