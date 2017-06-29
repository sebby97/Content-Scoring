import json
import sys
import os
from operator import itemgetter

groups = json.load(open(sys.argv[1]+'/scoringprofile.json'))['groups']
path = './'+sys.argv[1]+'/profiles/'

startingQuantum = []
totalEngagement = []
engagementVsAverage = []
engagementVsMax = []
engagementVsNetworkAverage = []
enagementVsNetworkMax = []
engagementVsScopeAverage = []
engagementVsScopeMax = []


for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            profileData = json.load(open('./'+sys.argv[1]+'/output/scores/engagementTotalTime/'+profile+'.json'))

            for postID in profileData.keys():

                postScoreData = profileData[postID]
                startingQuantum.append((postID,postScoreData['startingQuantum']))
                totalEngagement.append((postID,postScoreData['totalEngagement']))
                engagementVsAverage.append((postID,postScoreData['engagementVsAverage']))
                engagementVsMax.append((postID,postScoreData['engagementVsMax']))
                engagementVsNetworkAverage.append((postID,postScoreData['engagementVsNetworkAverage']))
                enagementVsNetworkMax.append((postID,postScoreData['enagementVsNetworkMax']))
                engagementVsScopeAverage.append((postID,postScoreData['engagementVsScopeAverage']))
                engagementVsScopeMax.append((postID,postScoreData['engagementVsScopeMax']))

startingQuantum = [x[0] for x in sorted(startingQuantum, key=lambda x: x[1],reverse=True)]
totalEngagement = [x[0] for x in sorted(totalEngagement, key=lambda x: x[1],reverse=True)]
engagementVsAverage = [x[0] for x in sorted(engagementVsAverage, key=lambda x: x[1],reverse=True)]
engagementVsMax = [x[0] for x in sorted(engagementVsMax, key=lambda x: x[1],reverse=True)]
engagementVsNetworkAverage = [x[0] for x in sorted(engagementVsNetworkAverage, key=lambda x: x[1],reverse=True)]
enagementVsNetworkMax = [x[0] for x in sorted(enagementVsNetworkMax, key=lambda x: x[1],reverse=True)]
engagementVsScopeAverage = [x[0] for x in sorted(engagementVsScopeAverage, key=lambda x: x[1],reverse=True)]
engagementVsScopeMax = [x[0] for x in sorted(engagementVsScopeMax, key=lambda x: x[1],reverse=True)]

outputData = {
    'startingQuantum':startingQuantum,
    'totalEngagement':totalEngagement,
    'engagementVsAverage':engagementVsAverage,
    'engagementVsMax':engagementVsMax,
    'engagementVsNetworkAverage':engagementVsNetworkAverage,
    'enagementVsNetworkMax':enagementVsNetworkMax,
    'engagementVsScopeAverage':engagementVsScopeAverage,
    'engagementVsScopeMax':engagementVsScopeMax
}

rankDirectory = './'+sys.argv[1]+'/output/ranks/'
if not os.path.exists(rankDirectory):
        os.mkdir(rankDirectory)
outputDirectory = rankDirectory+'engagementTotalTime/'
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)



with open(outputDirectory+'rank.json', 'w') as outputFile:
    json.dump(outputData, outputFile,indent = 4)
