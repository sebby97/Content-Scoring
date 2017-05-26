import json
import os
import sys

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

#Gets a list of all the profile paths...
profileList = [x[0] for x in os.walk('./../../profiles')]

del profileList[0]

#Loops through file directory and does neccessary calculations
for profile in profileList:
    #From the two files inside a individual's network records it opens postData file
    postData= json.load(open(profile+'/postData.json'))

    print(profile)

    #Determine the current social media being used and the ID of the individual
    network = profile.split("/")[4].split(".")[0]
    ID      = profile.split("/")[4].split(".")[1]

    #Counts engagement and posts by looping through posts in postData file
    for post in postData:
        #Value of the total engagement for a particular post in the postData collection
        #Note : Adjusted based on social media platform
        if network=='instagram':
            postEngagement = (post['likesRcvd'] + post['repliesRcvd'])
        elif network=='twitter':
            postEngagement = (post['likesRcvd'] + post['sharesRcvd'])
        else:
            postEngagement = (post['likesRcvd'] + post['repliesRcvd'] + post['sharesRcvd'])

        #Store the values for overall counts
        data['maxEngagementByNetwork'][network] = max(data['maxEngagementByNetwork'][network],postEngagement)
        data['totalEngagementByNetwork'][network] += postEngagement
        data['totalPostsByNetwork'][network] += 1

        #Earliest (smallest) time quantum
        data['startingQuantum'] = min(data['startingQuantum'],post['timeQuantum'])


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





################################################################################
#########################  WRITING INTO JSON FILE ##############################
#########################  (Taken from sys input) ##############################
################################################################################
with open('output.json', 'w') as outputFile:
    #Write to output file
    json.dump(data, outputFile)
