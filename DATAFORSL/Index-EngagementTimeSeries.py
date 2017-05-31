import json

################################################################################
#############  THESE ARE  THE COUNTERS FOR THE INFORMATION READ IN #############
################################################################################
data = {
    'averageEngagementByAge': [],
    'averageEngagementByAgeByNetwork':{
        'facebook_page':[]
        'twitter':[]
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
        'facebook_page':[]
        'twitter':[]
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
        'facebook_page':[]
        'twitter':[]
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
        'facebook_page':[]
        'twitter':[]
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










################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
with open('index-engagementTimeSeries.json', 'w') as outputFile:
    json.dump(data, outputFile,indent = 4)
