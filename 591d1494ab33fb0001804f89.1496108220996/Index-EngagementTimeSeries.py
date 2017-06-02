import json

################################################################################
#############  THESE ARE  THE COUNTERS FOR THE INFORMATION READ IN #############
################################################################################
data = {
    'averageEngagementByAge': [],
    'averageEngagementByAgeByNetwork':{
        'facebook_page':[],
        'twitter':[],
        'instagram':[]
    },
    'averageEngagementByAgeByScope': {
        'anchor': [],
        'brand': [],
        'individual': [],
        'sub-brand': []
    },

    'averageEngagementOverTime': [],
    'averageEngagementOverTimeByNetwork':{
        'facebook_page':[],
        'twitter':[],
        'instagram':[]
    },
    'averageEngagementOverTimeByScope': {
        'anchor': [],
        'brand': [],
        'individual': [],
        'sub-brand': []
    },

    'maxEngagementByAge': [],
    'maxEngagementByAgeByNetwork':{
        'facebook_page':[],
        'twitter':[],
        'instagram':[]
    },
    'maxEngagementByAgeByScope': {
        'anchor': [],
        'brand': [],
        'individual': [],
        'sub-brand': []
    },

    'maxEngagementOverTime': [],
    'maxEngagementOverTimeByNetwork':{
        'facebook_page':[],
        'twitter':[],
        'instagram':[]
    },
    'maxEngagementOverTimeByScope': {
        'anchor': [],
        'brand': [],
        'individual': [],
        'sub-brand': []
    },
    "startingQuantum":0
}

#Gets scoringprofile json file
scoringprofile= json.load(open('./scoringprofile.json'))

#list of all the groups that will be looped through
groups = scoringprofile['groups']

#Path to the profiles collection from the current directory where this
#python program is saved
path = './profiles/'

totalPosts = 0

postStartById = {}

engagementByAge = {}

for group in groups:
    assets = group['assets']
    for asset in assets:
        currAsset = group['assets'][asset]
        scope = currAsset['scope']

        profiles = list(filter(None,[currAsset.get('facebook'),currAsset.get('twitter'),currAsset.get('instagram')]))

        for profile in profiles:

            network = profile.split('.')[0]
            activityData = json.load(open(path+profile+'/activity.json'))

            postIDs = {}

            for activity in activityData:

                postEngagement = activity.get('likesRcvd',0)+activity.get('sharesRcvd',0)+activity.get('repliesRcvd',0)

                time = activity['timeQuantum']

                if activity['postidString'] not in postStartById:
                    postStartById[activity['postidString']] = time
                    totalPosts+=1

                age = (time - postStartById[activity['postidString']])//12

                if age in engagementByAge:
                    engagementByAge[age] += postEngagement
                else:
                    engagementByAge[age] = postEngagement

for x in range(0,max(engagementByAge.keys())):
    if x in engagementByAge:
        data['averageEngagementByAge'].append(engagementByAge[x]/totalPosts)
    else:
        data['averageEngagementByAge'].append(0)


################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
with open('index-engagementTimeSeries.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
