def initializePostAgeHours(totalAgeData):
    return [0]*totalAgeData
def initializeTimelineHours(startingQuantum,postStartQuantum):
    timeLine = []
    startHour = startingQuantum//12
    start = max(0,(postStartQuantum-startingQuantum)//12)

    for hour in range(start,168):
        timeLine.append({'epochHours':startHour+hour,'value':0})
    return timeLine

def initializePostScores(post_start,startingQuantum,totalAgeData,startAge):
    summary = {
        'post_start':post_start,
        'startAge':startAge,
        'totalAgeData':totalAgeData,
        'engagementByAge':initializePostAgeHours(totalAgeData),
        'engagementOverTime':initializeTimelineHours(startingQuantum,post_start),
        'engagementVsAverageByAge':initializePostAgeHours(totalAgeData),
        'engagementVsAverageByAgeByNetwork':initializePostAgeHours(totalAgeData),
        'engagementVsAverageByAgeByScope':initializePostAgeHours(totalAgeData),
        'engagementVsMaxByAge':initializePostAgeHours(totalAgeData),
        'engagementVsMaxByAgeByNetwork':initializePostAgeHours(totalAgeData),
        'engagementVsMaxByAgeByScope':initializePostAgeHours(totalAgeData),
        'engagementVsAverageOverTime':initializeTimelineHours(startingQuantum,post_start),
        'engagementVsAverageOverTimeByNetwork':initializeTimelineHours(startingQuantum,post_start),
        'engagementVsAverageOverTimeByScope':initializeTimelineHours(startingQuantum,post_start),
        'engagementVsMaxOverTime':initializeTimelineHours(startingQuantum,post_start),
        'engagementVsMaxOverTimeByNetwork':initializeTimelineHours(startingQuantum,post_start),
        'engagementVsMaxOverTimeByScope':initializeTimelineHours(startingQuantum,post_start)

    }
    return summary
