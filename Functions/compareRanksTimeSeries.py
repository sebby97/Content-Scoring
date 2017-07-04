import json
import sys

output1 = json.load(open(sys.argv[1]+'/output/ranks/engagementTimeSeries/ranks.json'))
output2 = json.load(open(sys.argv[1]+'/ranks/engagementTimeSeries/ranks.json'))



def recursiveCheck(output1,output2,path):
    for key in output1.keys():

        if('emerging' in key):
            continue
        if type(output1[key]) == type(dict()):
            if key not in output2:
                print("\n--"+path+'[\''+key+"\']--doesn't exist in Output 2\n")
            else:
                recursiveCheck(output1[key],output2[key],path+'[\''+key+'\']')
                continue

        if key not in output2:
            print("\nKey path --"+path+'[\''+key+"\']-- doesn't exist in input file 2\n")
        elif (output1[key] != output2[key] and key!='startingQuantum'):
            if type(output1[key])==type(list()):
                print(key)
                diffList = []
                for post in output1[key]:
                    index1 = output1[key].index(post)
                    index2 = output2[key].index(post)
                    diffList.append(index2 - index1)
                print(diffList)
                print(len(output1[key]))
                print(len(output2[key]))
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key][0:10])+'\t\nFile 2:\t'+str(output2[key][0:10])+'\n')

            elif type(output1[key])!=type(list()):
                print('\nOutput mismatch @ key path --'+path+'[\''+key+'\']--\nFile 1:\t'+str(output1[key])+'\tFile 2:\t'+str(output2[key])+'\n')



recursiveCheck(output1,output2,'')
