import json

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
scoringprofile= json.load(open('./scoringprofile.json'))

#list of all the groups that will be looped through
groups = scoringprofile['groups']

#Path to the profiles collection from the current directory where this
#python program is saved
path = './profiles/'


#Loops through the groups in the scoringprofile data
for group in groups:
    assets = group['assets']
    for asset in assets:

        currAsset = group['assets'][asset]

        scope = currAsset['scope']

        profiles = []

        if 'facebook' in currAsset:
            profiles.append(currAsset['facebook'])
        if 'twitter' in currAsset:
            profiles.append(currAsset['twitter'])
        if 'instagram' in currAsset:
            profiles.append(currAsset['instagram'])


        for profile in profiles:
            network = profile.split('.')[0]
            activityData = json.load(open(path+profile+'/activity.json'))


            postCountByID = {}
            postIDs = []
            for activity in activityData:

                postEngagement=0
                if 'likesRcvd' in activity:
                    postEngagement += activity['likesRcvd']
                if 'repliesRcvd' in activity:
                    postEngagement += activity['repliesRcvd']
                if 'sharesRcvd' in activity:
                    postEngagement += activity['sharesRcvd']

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


data['totalEngagement'] = data['totalEngagementByNetwork']['facebook_page']+data['totalEngagementByNetwork']['twitter']+data['totalEngagementByNetwork']['instagram']
data['maxEngagement'] = max(data['maxEngagementByNetwork']['facebook_page'],data['maxEngagementByNetwork']['twitter'],data['maxEngagementByNetwork']['instagram'])
data['totalPosts'] = data['totalPostsByNetwork']['facebook_page']+data['totalPostsByNetwork']['twitter']+data['totalPostsByNetwork']['instagram']

data['averageEngagement'] = data['totalEngagement']/data['totalPosts']
data['averageEngagementByNetwork']['facebook_page'] = data['totalEngagementByNetwork']['facebook_page']/data['totalPostsByNetwork']['facebook_page']
data['averageEngagementByNetwork']['twitter'] = data['totalEngagementByNetwork']['twitter']/data['totalPostsByNetwork']['twitter']
data['averageEngagementByNetwork']['instagram'] = data['totalEngagementByNetwork']['instagram']/data['totalPostsByNetwork']['instagram']

data['averageEngagementByScope']['anchor'] = data['totalEngagementByScope']['anchor']/data['totalPostsByScope']['anchor']
data['averageEngagementByScope']['brand'] = data['totalEngagementByScope']['brand']/data['totalPostsByScope']['brand']
data['averageEngagementByScope']['individual'] = data['totalEngagementByScope']['individual']/data['totalPostsByScope']['individual']
data['averageEngagementByScope']['sub-brand'] = data['totalEngagementByScope']['sub-brand']/data['totalPostsByScope']['sub-brand']






################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
with open('index-engagementTotalTime.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
