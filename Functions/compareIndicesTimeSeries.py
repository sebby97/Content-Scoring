import json
import sys

output1 = json.load(open(sys.argv[1]+'output/indices/engagementTimeSeries/index.json'))
output2 = json.load(open(sys.argv[1]+'indices/engagementTimeSeries/index.json'))

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
        elif output1[key] != output2[key]:
            if(type(output1[key])==type(list())):
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key][0:10])+'\tFile 2:\t'+str(output2[key][0:10])+'\n')
            else:
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key])+'\tFile 2:\t'+str(output2[key])+'\n')

recursiveCheck(output1,output2,'')
