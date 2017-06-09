import json
import sys
import os

data = {
    #Keeps track of total engagement and engagement by network
    'totalAudience' : 0
}

#Path to the profiles collection from the current directory where this
#python program is saved
path = './'+sys.argv[1]+'/profiles/'

groups = json.load(open('./'+sys.argv[1]+'/scoringprofile.json'))['groups']

#COUNTS TOTAL posts BY USING postCounter AND INITIALIZES postSummaries
for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            postData = json.load(open(path+profile+'/postData.json'))
            for post in postData:
                data['totalAudience'] += post.get('likesRcvd',0)+post.get('sharesRcvd',0)+post.get('repliesRcvd',0)


outputDirectory = './'+sys.argv[1]+'/output/'
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

with open(outputDirectory+'index-performanceMetrics.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
