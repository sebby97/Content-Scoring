import json
import sys

output1 = json.load(open(sys.argv[1]+'output/ranks/engagementTotalTime/rank.json'))
output2 = json.load(open(sys.argv[1]+'ranks/engagementTotalTime/ranks.json'))


def listDiff(list1, list2):
    indexDiff = []
    for i in range(0,len(list1)):
        if(list1[i]!=list2[i]):
            indexDiff.append(i)
    print(indexDiff)


def recursiveCheck(output1,output2,path):
    for key in output1.keys():
        if type(output1[key]) == type(dict()):
            if key not in output2:
                print("\n--"+path+'[\''+key+"\']--doesn't exist in Output 2\n")
            else:
                recursiveCheck(output1[key],output2[key],path+'[\''+key+'\']')
                continue

        if key not in output2:
            # print('hi')
            print("\nKey path --"+path+'[\''+key+"\']-- doesn't exist in input file 2\n")
        elif (output1[key] != output2[key] and key!='startingQuantum'):
            if type(output1[key])==type(list()):
                listDiff(output1[key],output2[key])
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key][0:10])+'\tFile 2:\t'+str(output2[key][0:10])+'\n')
            elif type(output1[key])!=type(list()):
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key])+'\tFile 2:\t'+str(output2[key])+'\n')



recursiveCheck(output1,output2,'')
