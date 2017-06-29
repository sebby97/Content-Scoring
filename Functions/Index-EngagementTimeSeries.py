import json
import sys
import os
from Index_HelperMethods import *


#####CHANGE CURRENT QUANTUM#####

#Data window information
snapshotTime = int(sys.argv[1].split('.')[len(sys.argv[1].split('.'))-1])
currentQuantum = snapshotTime//300000
weekTimeQuantum = 2015
startingQuantum = currentQuantum-weekTimeQuantum
currentHour = currentQuantum//12
startHour = startingQuantum//12

data = {
    'averageEngagementByAge': initializeAgeHours(),
    'averageEngagementByAgeByNetwork':{
        'facebook_page':initializeAgeHours(),
        'twitter':initializeAgeHours(),
        'instagram':initializeAgeHours()
    },
    'averageEngagementByAgeByScope': {
        'anchor': initializeAgeHours(),
        'brand': initializeAgeHours(),
        'individual': initializeAgeHours(),
        'sub-brand': initializeAgeHours()
    },

    'averageEngagementOverTime': initializeDataTimelineHours(startHour),
    'averageEngagementOverTimeByNetwork':{
        'facebook_page':initializeDataTimelineHours(startHour),
        'twitter':initializeDataTimelineHours(startHour),
        'instagram':initializeDataTimelineHours(startHour),
    },
    'averageEngagementOverTimeByScope': {
        'anchor': initializeDataTimelineHours(startHour),
        'brand': initializeDataTimelineHours(startHour),
        'individual': initializeDataTimelineHours(startHour),
        'sub-brand': initializeDataTimelineHours(startHour)
    },

    'maxEngagementByAge': initializeAgeHours(),
    'maxEngagementByAgeByNetwork':{
        'facebook_page':initializeAgeHours(),
        'twitter':initializeAgeHours(),
        'instagram':initializeAgeHours()
    },
    'maxEngagementByAgeByScope': {
        'anchor': initializeAgeHours(),
        'brand': initializeAgeHours(),
        'individual': initializeAgeHours(),
        'sub-brand': initializeAgeHours()
    },

    'maxEngagementOverTime': initializeDataTimelineHours(startHour),
    'maxEngagementOverTimeByNetwork':{
        'facebook_page':initializeDataTimelineHours(startHour),
        'twitter':initializeDataTimelineHours(startHour),
        'instagram':initializeDataTimelineHours(startHour)
    },
    'maxEngagementOverTimeByScope': {
        'anchor': initializeDataTimelineHours(startHour),
        'brand': initializeDataTimelineHours(startHour),
        'individual': initializeDataTimelineHours(startHour),
        'sub-brand': initializeDataTimelineHours(startHour)
    },
    'startingQuantum':startingQuantum
}

#Path to the profiles collection from the current directory where this
#python program is saved
path = './'+sys.argv[1]+'/profiles/'

#List of all networks and scopes for itiration
networks = ['facebook_page','twitter','instagram']
scopes = ['anchor', 'brand','individual','sub-brand']

#scoringprofile json file
scoringProfile = json.load(open('./'+sys.argv[1]+'/scoringprofile.json'))

#contains data about engagement by age, engagement overtime, and both my scopes/network
postSummaries = {}
postCounter = initializeCounter(startHour)
engagementCounter = initializeCounter(startHour)

groups = scoringProfile['groups']


#COUNTS TOTAL posts BY USING postCounter AND INITIALIZES postSummaries
for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            network = profile.split('.')[0]
            postData = json.load(open(path+profile+'/postData.json'))

            for post in postData:
                postidString = post['postidString']
                postTimestamp = post['timeQuantum']
                postStartHour = postTimestamp//12

                postSummaries[postidString] = initializePostSummary(scope, network, postTimestamp,startHour)
                # scope, network and postTimestamp are relevant to post
                # startHour is relevant to overall production...

                postCounter = updatePostCount(postCounter,network,scope,postStartHour,startHour,currentHour)

# COUNTS TOTAL engagement BY USING engagementCounter
for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            network = profile.split('.')[0]
            activityData = json.load(open(path+profile+'/activity.json'))

            for activity in activityData:
                postidString = activity['postidString']
                postEngagement = activity.get('likesRcvd',0)+activity.get('sharesRcvd',0)+activity.get('repliesRcvd',0)

                time = activity['timeQuantum']
                age = (time - postSummaries[postidString]['timestamp'])//12

                if(time<startingQuantum):
                    continue

                epochHourIndex = (time-startingQuantum)//12
                engagementCounter = updateEngagementCount(postEngagement,age,epochHourIndex,engagementCounter,network,scope)

                postSummaries[postidString]['engagementByAge'][age] += postEngagement
                postSummaries[postidString]['engagementOverTime'][epochHourIndex]['value'] += postEngagement


#CALCULATE AVERAGES BY AGE
for age in range (0,720):
    data['averageEngagementByAge'][age]=round(engagementCounter['ByAge']['Overall'][age]/max(postCounter['ByAge']['Overall'][age],1),3)
    for scope in scopes:
        data['averageEngagementByAgeByScope'][scope][age]=round(engagementCounter['ByAge']['Scope'][scope][age]/max(postCounter['ByAge']['Scope'][scope][age],1),3)
    for network in networks:
        data['averageEngagementByAgeByNetwork'][network][age]=round(engagementCounter['ByAge']['Network'][network][age]/max(postCounter['ByAge']['Network'][network][age],1),3)

#CALCULATE AVERAGES BY TIMELINE
for hour in range (0,168):
    epochHour = startHour+hour
    data['averageEngagementOverTime'][hour]['value']=round(engagementCounter['OverTime']['Overall'][hour]['value']/max(postCounter['OverTime']['Overall'][hour]['value'],1),3)
    for scope in scopes:
        data['averageEngagementOverTimeByScope'][scope][hour]['value']=round(engagementCounter['OverTime']['Scope'][scope][hour]['value']/max(postCounter['OverTime']['Scope'][scope][hour]['value'],1),3)
    for network in networks:
        data['averageEngagementOverTimeByNetwork'][network][hour]['value']=round(engagementCounter['OverTime']['Network'][network][hour]['value']/max(postCounter['OverTime']['Network'][network][hour]['value'],1),3)

#FIND MAX OF EACH PROPERTY BY ITERATING THROUGH ALL POSTS AND THEIR SUMMARIES
for post in postSummaries:

    network = postSummaries[post]['network']
    scope = postSummaries[post]['scope']

    for age in range(0,720):
        currentEngagement = postSummaries[post]['engagementByAge'][age]
        data['maxEngagementByAge'][age] = max(currentEngagement,data['maxEngagementByAge'][age])
        data['maxEngagementByAgeByNetwork'][network][age] = max(currentEngagement,data['maxEngagementByAgeByNetwork'][network][age])
        data['maxEngagementByAgeByScope'][scope][age] = max(currentEngagement,data['maxEngagementByAgeByScope'][scope][age])

    for hour in range(0,168):
        epochHour = startHour+hour
        currentEngagement = postSummaries[post]['engagementOverTime'][hour]['value']
        if(currentEngagement>data['maxEngagementOverTime'][hour]['value']):
            data['maxEngagementOverTime'][hour]['value'] = currentEngagement
        if(currentEngagement>data['maxEngagementOverTimeByNetwork'][network][hour]['value']):
            data['maxEngagementOverTimeByNetwork'][network][hour]['value'] = currentEngagement
        if(currentEngagement>data['maxEngagementOverTimeByScope'][scope][hour]['value']):
            data['maxEngagementOverTimeByScope'][scope][hour]['value'] = currentEngagement

################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
outputDirectory = './'+sys.argv[1]+'/output/'
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
indexDirectory = './'+sys.argv[1]+'/output/indices/'
if not os.path.exists(indexDirectory):
        os.mkdir(indexDirectory)
timeSeriesDirectory = './'+sys.argv[1]+'/output/indices/engagementTimeSeries/'
if not os.path.exists(timeSeriesDirectory):
        os.mkdir(timeSeriesDirectory)

with open(timeSeriesDirectory+'index.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
