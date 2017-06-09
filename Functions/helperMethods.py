def epochHours(timeQuantum):
    return timeQuantum//12

def initializeAgeHours():
    return [0]*720
def initializeTimelineHours(startHour):
    timeLine = {}
    for hour in range(startHour,startHour+168):
        timeLine[hour] = 0
    return timeLine
def initializeDataTimelineHours():
    return [{'epochHour':0,'value':0}]*168
def initializePostSummary(scope_of_post, network_of_post, post_start,startHour):
    summary = {
        'timestamp':post_start,
        'scope':scope_of_post,
        'network':network_of_post,
        'engagementByAge':initializeAgeHours(),
        'engagementOverTime':initializeTimelineHours(startHour)
    }
    return summary
def initializeCounter(startHour):
    counter = {
        'ByAge': {
            'Overall':initializeAgeHours(),
            'Scope': {
                'anchor':initializeAgeHours(),
                'brand':initializeAgeHours(),
                'individual':initializeAgeHours(),
                'sub-brand':initializeAgeHours()
            },
            'Network':{
                'facebook_page':initializeAgeHours(),
                'twitter':initializeAgeHours(),
                'instagram':initializeAgeHours()
            }
        },
        'OverTime': {
            'Overall':initializeTimelineHours(startHour),
            'Scope': {
                'anchor':initializeTimelineHours(startHour),
                'brand':initializeTimelineHours(startHour),
                'individual':initializeTimelineHours(startHour),
                'sub-brand':initializeTimelineHours(startHour)
            },
            'Network':{
                'facebook_page':initializeTimelineHours(startHour),
                'twitter':initializeTimelineHours(startHour),
                'instagram':initializeTimelineHours(startHour)
            }
        }
    }
    return counter

def updatePostCount(network,scope,postCountTracker,startingHour,postStartHour,currentHour):

    for epochHour in range(max(startingHour, postStartHour),currentHour+1):
        age = epochHour - postStartHour

        postCountTracker['OverTime']['Overall'][epochHour] += 1
        postCountTracker['OverTime']['Network'][network][epochHour] += 1
        postCountTracker['OverTime']['Scope'][scope][epochHour] += 1

        postCountTracker['ByAge']['Overall'][age] += 1
        postCountTracker['ByAge']['Network'][network][age] += 1
        postCountTracker['ByAge']['Scope'][scope][age] += 1

    return postCountTracker

def updateEngagementCount(postEngagement,age,epochHour,totalEngagementCounts,network,scope):


    totalEngagementCounts['ByAge']['Overall'][age] += postEngagement
    totalEngagementCounts['ByAge']['Network'][network][age] += postEngagement
    totalEngagementCounts['ByAge']['Scope'][scope][age] += postEngagement

    totalEngagementCounts['OverTime']['Overall'][epochHour] += postEngagement
    totalEngagementCounts['OverTime']['Network'][network][epochHour] += postEngagement
    totalEngagementCounts['OverTime']['Scope'][scope][epochHour] += postEngagement


    return totalEngagementCounts
