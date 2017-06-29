import json
import sys
import os

index_engagementTotalTime = json.load(open('./'+sys.argv[1]+'/output/indices/engagementTotalTime/index.json'))
startingQuantum = index_engagementTotalTime['startingQuantum']

groups = json.load(open('./'+sys.argv[1]+'/scoringprofile.json'))['groups']

#############################################################
################## CREATE OUTPUT DIRECTORY ##################
#############################################################

path = './'+sys.argv[1]+'/profiles/'
outputDirectory = './'+sys.argv[1]+'/output/scores/engagementTotalTime/'
if not os.path.exists('./'+sys.argv[1]+'/output/scores/'):
        os.mkdir('./'+sys.argv[1]+'/output/scores/')
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)


for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            postData = json.load(open(path+profile+'/postData.json'))
            postInfo = {}

            for post in postData:
                postID = post['postidString']
                postInfo[postID] = {
                    'startQuantum':post['timeQuantum'],
                    'network':profile.split('.')[0],
                    'totalEngagement':0

                }

            activityData = json.load(open(path+profile+'/activity.json'))
            for activity in activityData:
                postID = activity['postidString']
                postEngagement = activity.get('likesRcvd',0)+activity.get('sharesRcvd',0)+activity.get('repliesRcvd',0)
                postStartQuantum = postInfo[postID]['startQuantum']

                postInfo[postID]['totalEngagement'] += postEngagement


            dataTotalTime = {}

            for postID in postInfo:
                totalEngagement = postInfo[postID]['totalEngagement']
                network = postInfo[postID]['network']
                dataTotalTime[postID] = {}
                dataTotalTime[postID]['startingQuantum'] = max(startingQuantum, postInfo[postID]['startQuantum'])
                dataTotalTime[postID]['totalEngagement'] = totalEngagement
                dataTotalTime[postID]['engagementVsAverage'] = round(totalEngagement/max(index_engagementTotalTime['averageEngagement'],1),3)
                dataTotalTime[postID]['engagementVsMax'] = round(totalEngagement/max(index_engagementTotalTime['maxEngagement'],1),3)
                dataTotalTime[postID]['engagementVsNetworkAverage'] = round(totalEngagement/max(index_engagementTotalTime['averageEngagementByNetwork'][network],1),3)
                dataTotalTime[postID]['enagementVsNetworkMax'] = round(totalEngagement/max(index_engagementTotalTime['maxEngagementByNetwork'][network],1),3)
                dataTotalTime[postID]['engagementVsScopeAverage'] = round(totalEngagement/max(index_engagementTotalTime['averageEngagementByScope'][scope],1),3)
                dataTotalTime[postID]['engagementVsScopeMax'] = round(totalEngagement/max(index_engagementTotalTime['maxEngagementByScope'][scope],1),3)


            with open(outputDirectory+profile+'.json', 'w') as outputFile:
                json.dump(dataTotalTime, outputFile,indent = 4)
