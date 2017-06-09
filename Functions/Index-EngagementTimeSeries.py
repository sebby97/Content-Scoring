import json
import sys
import os
from helperMethods import *

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

    'averageEngagementOverTime': initializeDataTimelineHours(),
    'averageEngagementOverTimeByNetwork':{
        'facebook_page':initializeDataTimelineHours(),
        'twitter':initializeDataTimelineHours(),
        'instagram':initializeDataTimelineHours(),
    },
    'averageEngagementOverTimeByScope': {
        'anchor': initializeDataTimelineHours(),
        'brand': initializeDataTimelineHours(),
        'individual': initializeDataTimelineHours(),
        'sub-brand': initializeDataTimelineHours()
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

    'maxEngagementOverTime': [{'epochHour':0,'value':0}]*168,
    'maxEngagementOverTimeByNetwork':{
        'facebook_page':[{'epochHour':0,'value':0}]*168,
        'twitter':[{'epochHour':0,'value':0}]*168,
        'instagram':[{'epochHour':0,'value':0}]*168
    },
    'maxEngagementOverTimeByScope': {
        'anchor': [{'epochHour':0,'value':0}]*168,
        'brand': [{'epochHour':0,'value':0}]*168,
        'individual': [{'epochHour':0,'value':0}]*168,
        'sub-brand': [{'epochHour':0,'value':0}]*168
    },
    'startingQuantum':0
}

#Data window information
currentQuantum = 1496709420185//300000
startingQuantum = currentQuantum-2016+12
data['startingQuantum']=startingQuantum
currentHour = currentQuantum//12
startingHour = startingQuantum//12

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
postCounter = initializeCounter(startingHour)
engagementCounter = initializeCounter(startingHour)

groups = scoringProfile['groups']

count = 0

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
                count+=1
                postidString = post['postidString']
                postTimestamp = post['timeQuantum']
                postStartHour = postTimestamp//12+1
                postSummaries[postidString] = initializePostSummary(scope, network, postTimestamp,startingHour)

                postCounter = updatePostCount(network,scope,postCounter,startingHour,postStartHour,currentHour)

#COUNTS TOTAL engagement BY USING engagementCounter
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
                if(time<startingQuantum):
                    continue

                age = (time - postSummaries[postidString]['timestamp'])//12
                activityEpochHour = time//12
                engagementCounter = updateEngagementCount(postEngagement,age,activityEpochHour,engagementCounter,network,scope)

                postSummaries[postidString]['engagementByAge'][age] += postEngagement
                postSummaries[postidString]['engagementOverTime'][activityEpochHour] += postEngagement


#CALCULATE AVERAGES BY AGE
for age in range (0,720):
    data['averageEngagementByAge'][age]=round(engagementCounter['ByAge']['Overall'][age]/max(postCounter['ByAge']['Overall'][age],1),3)
    for scope in scopes:
        data['averageEngagementByAgeByScope'][scope][age]=round(engagementCounter['ByAge']['Scope'][scope][age]/max(postCounter['ByAge']['Scope'][scope][age],1),3)
    for network in networks:
        data['averageEngagementByAgeByNetwork'][network][age]=round(engagementCounter['ByAge']['Network'][network][age]/max(postCounter['ByAge']['Network'][network][age],1),3)

#CALCULATE AVERAGES BY TIMELINE
for hour in range (0,168):
    epochHour = startingHour+hour
    data['averageEngagementOverTime'][hour]={'epochHour':epochHour, 'value':engagementCounter['OverTime']['Overall'][epochHour]}
    for scope in scopes:
        data['averageEngagementOverTimeByScope'][scope][hour]={'epochHour':epochHour, 'value':round(engagementCounter['OverTime']['Scope'][scope][epochHour]/max(postCounter['OverTime']['Scope'][scope][epochHour],1),3)}
    for network in networks:
        data['averageEngagementOverTimeByNetwork'][network][hour]={'epochHour':epochHour, 'value':round(engagementCounter['OverTime']['Network'][network][epochHour]/max(postCounter['OverTime']['Network'][network][epochHour],1),3)}

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
        epochHour = startingHour+hour
        currentEngagement = postSummaries[post]['engagementOverTime'][epochHour]
        if(currentEngagement>data['maxEngagementOverTime'][hour]['value']):
            data['maxEngagementOverTime'][hour] = {'epochHour':epochHour,'value':currentEngagement}
        if(currentEngagement>data['maxEngagementOverTimeByNetwork'][network][hour]['value']):
            data['maxEngagementOverTimeByNetwork'][network][hour] = {'epochHour':epochHour,'value':currentEngagement}
        if(currentEngagement>data['maxEngagementOverTimeByScope'][scope][hour]['value']):
            data['maxEngagementOverTimeByScope'][scope][hour] = {'epochHour':epochHour,'value':currentEngagement}

################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
outputDirectory = './'+sys.argv[1]+'/output/'
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)


with open(outputDirectory+'index-engagementTimeSeries.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
