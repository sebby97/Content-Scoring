def initializeAgeHours():
    return [0]*720

def initializeDataTimelineHours(startHour):
    timelineHours = []
    for hour in range(0,168):
        timelineHours.append({'epochHour':startHour+hour,'value':0})
    return timelineHours

def initializePostSummary(scope_of_post, network_of_post, post_start,startHour):
    summary = {
        'timestamp':post_start,
        'scope':scope_of_post,
        'network':network_of_post,
        'engagementByAge':initializeAgeHours(),
        'engagementOverTime':initializeDataTimelineHours(startHour)
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
            'Overall':initializeDataTimelineHours(startHour),
            'Scope': {
                'anchor':initializeDataTimelineHours(startHour),
                'brand':initializeDataTimelineHours(startHour),
                'individual':initializeDataTimelineHours(startHour),
                'sub-brand':initializeDataTimelineHours(startHour)
            },
            'Network':{
                'facebook_page':initializeDataTimelineHours(startHour),
                'twitter':initializeDataTimelineHours(startHour),
                'instagram':initializeDataTimelineHours(startHour)
            }
        }
    }
    return counter

def updatePostCount(postCounter,network,scope,postStartHour,startHour,currentHour):

    for epochHour in range(max(startHour, postStartHour),currentHour):
        age = epochHour - postStartHour
        epochHourIndex = epochHour-startHour

        postCounter['OverTime']['Overall'][epochHourIndex]['value'] += 1
        postCounter['OverTime']['Network'][network][epochHourIndex]['value'] += 1
        postCounter['OverTime']['Scope'][scope][epochHourIndex]['value'] += 1

        postCounter['ByAge']['Overall'][age] += 1
        postCounter['ByAge']['Network'][network][age] += 1
        postCounter['ByAge']['Scope'][scope][age] += 1

    return postCounter

def updateEngagementCount(postEngagement,age,epochHourIndex,totalEngagementCounts,network,scope):



    totalEngagementCounts['ByAge']['Overall'][age] += postEngagement
    totalEngagementCounts['ByAge']['Network'][network][age] += postEngagement
    totalEngagementCounts['ByAge']['Scope'][scope][age] += postEngagement

    totalEngagementCounts['OverTime']['Overall'][epochHourIndex]['value'] += postEngagement
    totalEngagementCounts['OverTime']['Network'][network][epochHourIndex]['value'] += postEngagement
    totalEngagementCounts['OverTime']['Scope'][scope][epochHourIndex]['value'] += postEngagement


    return totalEngagementCounts
