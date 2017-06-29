import json
import sys
import os
from Score_HelperMethods import *

index_engagementTimeSeries = json.load(open('./'+sys.argv[1]+'/output/indices/engagementTimeSeries/index.json'))

snapshotTime = int(sys.argv[1].split('.')[len(sys.argv[1].split('.'))-1])
currentQuantum = snapshotTime//300000
startingQuantum = currentQuantum-2015
currentHour = currentQuantum//12

#############################################################
################## CREATE OUTPUT DIRECTORY ##################
#############################################################

path = './'+sys.argv[1]+'/profiles/'
outputDirectory = './'+sys.argv[1]+'/output/scores/engagementTimeSeries/'
if not os.path.exists('./'+sys.argv[1]+'/output/scores/'):
        os.mkdir('./'+sys.argv[1]+'/output/scores/')
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)



#############################################################
##################### SCORING ALGORITHM #####################
#############################################################

groups = json.load(open('./'+sys.argv[1]+'/scoringprofile.json'))['groups']
for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            postData = json.load(open(path+profile+'/postData.json'))
            postInfo = {}
            engagementByAge = {}
            engagementOverTime = {}

            for post in postData:
                postID = post['postidString']
                network = profile.split('.')[0]
                postTimestamp = post['timeQuantum']

                ageStart = max((startingQuantum-postTimestamp )//12,0)

                ageFinal = min(720,(currentQuantum-postTimestamp)//12+1)

                totalAgeData = ageFinal-ageStart
                engagementByAge[postID] = initializePostAgeHours(totalAgeData)
                engagementOverTime[postID] = initializeTimelineHours(startingQuantum,postTimestamp)
                postInfo[postID] = {
                    'startAge':ageStart,
                    'totalAgeData':totalAgeData,
                    'postTimestamp':postTimestamp,
                    'network':network,
                    'totalEngagementSinceQuantum':0
                }
            activityData = json.load(open(path+profile+'/activity.json'))
            for activity in activityData:
                postID = activity['postidString']
                postEngagement = activity.get('likesRcvd',0)+activity.get('sharesRcvd',0)+activity.get('repliesRcvd',0)
                time = activity['timeQuantum']
                postTimestamp = postInfo[postID]['postTimestamp']

                if(time<startingQuantum):
                    continue

                age = (time - postTimestamp)//12-postInfo[postID]['startAge']
                engagementByAge[postID][age] += postEngagement


                start = max(startingQuantum,postTimestamp)
                epochHourIndex = (time-start)//12
                postInfo[postID]['totalEngagementSinceQuantum'] += postEngagement
                engagementOverTime[postID][epochHourIndex]['value'] += postEngagement


            dataTimeSeries = {}

            for postID in postInfo:

                if(postInfo[postID]['totalEngagementSinceQuantum']==0):
                    continue
                postTimestamp = postInfo[postID]['postTimestamp']

                network = postInfo[postID]['network']
                dataTimeSeries[postID] = initializePostScores(postTimestamp,startingQuantum,postInfo[postID]['totalAgeData'],postInfo[postID]['startAge'])
                for age in range(0,postInfo[postID]['totalAgeData']):
                    dataTimeSeries[postID]['engagementByAge'][age] = engagementByAge[postID][age]
                    dataTimeSeries[postID]['engagementVsAverageByAge'][age]=round(engagementByAge[postID][age]/max(index_engagementTimeSeries['averageEngagementByAge'][age],1),3)
                    dataTimeSeries[postID]['engagementVsAverageByAgeByNetwork'][age]=round(engagementByAge[postID][age]/max(index_engagementTimeSeries['averageEngagementByAgeByNetwork'][network][age],1),3)
                    dataTimeSeries[postID]['engagementVsAverageByAgeByScope'][age]=round(engagementByAge[postID][age]/max(index_engagementTimeSeries['averageEngagementByAgeByScope'][scope][age],1),3)
                    dataTimeSeries[postID]['engagementVsMaxByAge'][age]=round(engagementByAge[postID][age]/max(index_engagementTimeSeries['maxEngagementByAge'][age],1),3)
                    dataTimeSeries[postID]['engagementVsMaxByAgeByNetwork'][age]=round(engagementByAge[postID][age]/max(index_engagementTimeSeries['maxEngagementByAgeByNetwork'][network][age],1),3)
                    dataTimeSeries[postID]['engagementVsMaxByAgeByScope'][age]=round(engagementByAge[postID][age]/max(index_engagementTimeSeries['maxEngagementByAgeByScope'][scope][age],1),3)

                startTimeline = max(0,(postTimestamp-startingQuantum)//12)
                maxHourIndex = min(currentQuantum-postTimestamp,168)
                for epochHour in range(startTimeline,maxHourIndex):

                    epochHourIndex = epochHour-startTimeline

                    dataTimeSeries[postID]['engagementOverTime'][epochHourIndex]['value']= engagementOverTime[postID][epochHourIndex]['value']
                    dataTimeSeries[postID]['engagementVsAverageOverTime'][epochHourIndex]['value']= round(engagementOverTime[postID][epochHourIndex]['value']/max(index_engagementTimeSeries['averageEngagementOverTime'][epochHourIndex]['value'],1),3)
                    dataTimeSeries[postID]['engagementVsAverageOverTimeByNetwork'][epochHourIndex]['value']= round(engagementOverTime[postID][epochHourIndex]['value']/max(index_engagementTimeSeries['averageEngagementOverTimeByNetwork'][network][epochHourIndex]['value'],1),3)
                    dataTimeSeries[postID]['engagementVsAverageOverTimeByScope'][epochHourIndex]['value']= round(engagementOverTime[postID][epochHourIndex]['value']/max(index_engagementTimeSeries['averageEngagementOverTimeByScope'][scope][epochHourIndex]['value'],1),3)
                    dataTimeSeries[postID]['engagementVsMaxOverTime'][epochHourIndex]['value']= round(engagementOverTime[postID][epochHourIndex]['value']/max(index_engagementTimeSeries['maxEngagementOverTime'][epochHourIndex]['value'],1),3)
                    dataTimeSeries[postID]['engagementVsMaxOverTimeByNetwork'][epochHourIndex]['value']= round(engagementOverTime[postID][epochHourIndex]['value']/max(index_engagementTimeSeries['maxEngagementOverTimeByNetwork'][network][epochHourIndex]['value'],1),3)
                    dataTimeSeries[postID]['engagementVsMaxOverTimeByScope'][epochHourIndex]['value']= round(engagementOverTime[postID][epochHourIndex]['value']/max(index_engagementTimeSeries['maxEngagementOverTimeByScope'][scope][epochHourIndex]['value'],1),3)



            with open(outputDirectory+profile+'.json', 'w') as outputFile:
                json.dump(dataTimeSeries, outputFile,indent = 4)
