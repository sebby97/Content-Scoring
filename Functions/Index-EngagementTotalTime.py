import json
import sys
import os

################################################################################
#############  THESE ARE  THE COUNTERS FOR THE INFORMATION READ IN #############
################################################################################

#Keeps track of the engagements for each of the social media platforms
data = {
    #Keeps track of total engagement and engagement by network
    'totalEngagement' : 0,
    'totalEngagementByNetwork' : {
        'facebook_page': 0,
        'instagram': 0,
        'twitter': 0
    },
    'totalEngagementByScope': {
        'anchor': 0,
        'brand': 0,
        'individual': 0,
        'sub-brand': 0
    },
    #Keeps track of the max number of engagements from all social media platforms
    'maxEngagement' : 0,
    'maxEngagementByNetwork' : {
        'facebook_page' : 0,
        'instagram': 0,
        'twitter':0
    },
    'maxEngagementByScope': {
        'anchor': 0,
        'brand': 0,
        'individual': 0,
        'sub-brand': 0
    },
    #Keeps track of number of posts in any particular network
    'totalPosts' : 0,
    'totalPostsByNetwork' : {
        'facebook_page' : 0,
        'instagram': 0,
        'twitter':0
    },
    'totalPostsByScope': {
        'anchor': 0,
        'brand': 0,
        'individual': 0,
        'sub-brand': 0
    },
    #Keeps track of averageEngagementByNetwork
    'averageEngagement' : 0,
    'averageEngagementByNetwork' : {
        'facebook_page': 0,
        'instagram': 0,
        'twitter': 0
    },
    'averageEngagementByScope': {
        'anchor': 0,
        'brand': 0,
        'individual': 0,
        'sub-brand': 0
    },
    #Starting quantum... initiated to infinity (min of all time quantums used)
    #probably a better way to do this
    'startingQuantum':float("inf")
}
################################################################################
#############  THIS WILL LOOP THROUGH THE PROFILES DIRECTORY AND ###############
#############    RECORD INFORMATION TO THE COUNTERS AS WELL AS   ###############
#############      KEEP TRACK OF INDIVIDUAL RECORDS                #############
################################################################################

#Gets scoringprofile json file
scoringprofile= json.load(open('./'+sys.argv[1]+'/scoringprofile.json'))
#list of all the groups that will be looped through
groups = scoringprofile['groups']
#Path to the profiles collection from the current directory where this
#python program is saved
path = './'+sys.argv[1]+'/profiles/'


#Loops through the groups in the scoringprofile data
for group in groups:
    for asset in group['assets']:

        currAsset = group['assets'][asset]
        scope = currAsset['scope']
        profiles = list(filter(None,[currAsset.get('facebook'),currAsset.get('twitter'),currAsset.get('instagram')]))

        for profile in profiles:

            network = profile.split('.')[0]
            activityData = json.load(open(path+profile+'/activity.json'))

            postCountByID = {}
            postIDs = []
            for activity in activityData:

                postEngagement = activity.get('likesRcvd',0)+activity.get('sharesRcvd',0)+activity.get('repliesRcvd',0)
                #Store the values for overall counts by network
                data['totalEngagementByNetwork'][network] += postEngagement
                #Store the values for overall counts by scopes
                data['totalEngagementByScope'][scope] += postEngagement

                if activity['postidString'] not in postCountByID:
                    postCountByID[activity['postidString']] = postEngagement
                    postIDs.append(activity['postidString'])
                    data['totalPostsByNetwork'][network] += 1
                    data['totalPostsByScope'][scope] += 1
                else:
                    postCountByID[activity['postidString']] += postEngagement

                #Earliest (smallest) time quantum
                data['startingQuantum'] = min(data['startingQuantum'],activity['timeQuantum'])
            maxPost = 0
            for ID in postIDs:
                if(postCountByID[ID]>maxPost):
                    maxPost = postCountByID[ID]
            data['maxEngagementByNetwork'][network]= max(data['maxEngagementByNetwork'][network],maxPost)
            data['maxEngagementByScope'][scope]= max(data['maxEngagementByScope'][scope],maxPost)




################################################################################
#########################  Some Basic calculations #############################
################################################################################


data['totalEngagement'] = data['totalEngagementByNetwork']['facebook_page'] + data['totalEngagementByNetwork']['twitter'] + data['totalEngagementByNetwork']['instagram']
data['maxEngagement'] = max(data['maxEngagementByNetwork']['facebook_page'] , data['maxEngagementByNetwork']['twitter'] , data['maxEngagementByNetwork']['instagram'])
data['totalPosts'] = data['totalPostsByNetwork']['facebook_page'] + data['totalPostsByNetwork']['twitter'] + data['totalPostsByNetwork']['instagram']


#Average Engagement overall, by network, and by scope rounded to three decimal places
data['averageEngagement'] = round(data['totalEngagement']/data['totalPosts'],3)

data['averageEngagementByNetwork']['facebook_page'] = round(data['totalEngagementByNetwork']['facebook_page']/data['totalPostsByNetwork']['facebook_page'],3)
data['averageEngagementByNetwork']['twitter'] = round(data['totalEngagementByNetwork']['twitter']/data['totalPostsByNetwork']['twitter'],3)
data['averageEngagementByNetwork']['instagram'] = round(data['totalEngagementByNetwork']['instagram']/data['totalPostsByNetwork']['instagram'],3)

data['averageEngagementByScope']['anchor'] = round(data['totalEngagementByScope']['anchor']/data['totalPostsByScope']['anchor'],3)
data['averageEngagementByScope']['brand'] = round(data['totalEngagementByScope']['brand']/data['totalPostsByScope']['brand'],3)
data['averageEngagementByScope']['individual'] = round(data['totalEngagementByScope']['individual']/data['totalPostsByScope']['individual'],3)
data['averageEngagementByScope']['sub-brand'] = round(data['totalEngagementByScope']['sub-brand']/data['totalPostsByScope']['sub-brand'],3)






################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
outputDirectory = './'+sys.argv[1]+'/output/'
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

with open(outputDirectory+'index-engagementTotalTime.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
