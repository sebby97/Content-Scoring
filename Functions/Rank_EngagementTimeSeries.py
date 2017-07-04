import json
import sys
import os
from operator import itemgetter

groups = json.load(open(sys.argv[1]+'/scoringprofile.json'))['groups']
path = './'+sys.argv[1]+'/profiles/'

snapshotTime = int(sys.argv[1].split('.')[len(sys.argv[1].split('.'))-1])
currentQuantum = snapshotTime//300000
freshPostTime = currentQuantum-144

###STORES ALL PAIRS OF (POSTID,value)###

emerging = []
emergingByScope = []
emergingByNetwork = []
topSixHour = []
topOneDay = []
topOneWeek = []
topSixHourByScope = []
topOneDayByScope = []
topOneWeekByScope = []
topSixHourByNetwork = []
topOneDayByNetwork = []
topOneWeekByNetwork = []

###ITERATE THROUGH ALL ASSETS AND PROFILES
for group in groups:
    for asset in group['assets']:
        currentAsset = group['assets'][asset]
        scope = currentAsset['scope']
        assetProfiles = list( filter( None,[currentAsset.get('facebook'),currentAsset.get('twitter'),currentAsset.get('instagram')] ) )

        for profile in assetProfiles:
            profileData = json.load(open('./'+sys.argv[1]+'/scores/engagementTimeSeries/'+profile+'.json'))
            network = profile.split('.')[0]

            ####LOOPS THROUGH ALL POSTS IN PROFILE###
            for postID in profileData.keys():

                postScoreData = profileData[postID]

                #postTimestamp = postScoreData['post_start']
                postTimestamp = postScoreData['startingQuantum']

                ###KEEPS TRACK OF ALL THE TOTAL RATIOS BY CATEGORY###
                sixHour = 0
                oneDay = 0
                oneWeek = 0
                sixHourScope = 0
                sixHourNetwork = 0
                oneDayScope = 0
                oneDayNetwork = 0
                oneWeekScope = 0
                oneWeekNetwork = 0
                emergingPost = 0
                emergingPostByScope = 0
                emergingPostByNetwork = 0

                #LOOPS THROUGH EACH TIME FRAME (Max of 168 which is 1 week of hours)

                dataLength = len(postScoreData['engagementVsAverageOverTime'])
                ageLength = len(postScoreData['engagementVsAverageByAgeByScope'])
                for hour in range(dataLength-1,-1,-1):
                    if(hour>=dataLength-6):
                        sixHour += postScoreData['engagementVsAverageOverTime'][hour]['value']
                        sixHourScope += postScoreData['engagementVsAverageOverTimeByScope'][hour]['value']
                        sixHourNetwork += postScoreData['engagementVsAverageOverTimeByNetwork'][hour]['value']
                        emergingPost += postScoreData['engagementVsAverageByAge'][hour]
                        emergingPostByScope +=postScoreData['engagementVsAverageByAgeByScope'][hour]
                        emergingPostByNetwork +=postScoreData['engagementVsAverageByAgeByNetwork'][hour]
                    if(hour>=dataLength-24):
                        oneDay += postScoreData['engagementVsAverageOverTime'][hour]['value']
                        oneDayScope += postScoreData['engagementVsAverageOverTimeByScope'][hour]['value']
                        oneDayNetwork += postScoreData['engagementVsAverageOverTimeByNetwork'][hour]['value']
                    if(hour>=dataLength-168):
                        oneWeek += postScoreData['engagementVsAverageOverTime'][hour]['value']
                        oneWeekScope += postScoreData['engagementVsAverageOverTimeByScope'][hour]['value']
                        oneWeekNetwork += postScoreData['engagementVsAverageOverTimeByNetwork'][hour]['value']

                topSixHour.append((postID,sixHour))
                topOneDay.append((postID,oneDay))
                topOneWeek.append((postID,oneWeek))
                topSixHourByScope.append((postID,sixHourScope))
                topOneDayByScope.append((postID,oneDayScope))
                topOneWeekByScope.append((postID,oneWeekScope))
                topSixHourByNetwork.append((postID,sixHourNetwork))
                topOneDayByNetwork.append((postID,oneDayNetwork))
                topOneWeekByNetwork.append((postID,oneWeekNetwork))

                #freshPostTime is the current hour - 12 hours
                if(postTimestamp>=freshPostTime):
                    emerging.append((postID,emergingPost))
                    emergingByScope.append((postID,emergingPostByScope))
                    emergingByNetwork.append((postID,emergingPostByNetwork))


# emerging = [x for x in sorted(emerging, key=lambda x: x[1],reverse=True)]
# emergingByScope = [x for x in sorted(emergingByScope, key=lambda x: x[1],reverse=True)]
# emergingByNetwork = [x for x in sorted(emergingByNetwork, key=lambda x: x[1],reverse=True)]
# topSixHour = [x for x in sorted(topSixHour, key=lambda x: x[1],reverse=True)]
# topOneDay = [x for x in sorted(topOneDay, key=lambda x: x[1],reverse=True)]
# topOneWeek = [x for x in sorted(topOneWeek, key=lambda x: x[1],reverse=True)]
# topSixHourByScope = [x for x in sorted(topSixHourByScope, key=lambda x: x[1],reverse=True)]
# topOneDayByScope = [x for x in sorted(topOneDayByScope, key=lambda x: x[1],reverse=True)]
# topOneWeekByScope = [x for x in sorted(topOneWeekByScope, key=lambda x: x[1],reverse=True)]
# topSixHourByNetwork = [x for x in sorted(topSixHourByNetwork, key=lambda x: x[1],reverse=True)]
# topOneDayByNetwork = [x for x in sorted(topOneDayByNetwork, key=lambda x: x[1],reverse=True)]
# topOneWeekByNetwork = [x for x in sorted(topOneWeekByNetwork, key=lambda x: x[1],reverse=True)]

emerging = [x[0] for x in sorted(emerging, key=lambda x: x[1],reverse=True)]
emergingByScope = [x[0] for x in sorted(emergingByScope, key=lambda x: x[1],reverse=True)]
emergingByNetwork = [x[0] for x in sorted(emergingByNetwork, key=lambda x: x[1],reverse=True)]
topSixHour = [x[0] for x in sorted(topSixHour, key=lambda x: x[1],reverse=True)]
topOneDay = [x[0] for x in sorted(topOneDay, key=lambda x: x[1],reverse=True)]
topOneWeek = [x[0] for x in sorted(topOneWeek, key=lambda x: x[1],reverse=True)]
topSixHourByScope = [x[0] for x in sorted(topSixHourByScope, key=lambda x: x[1],reverse=True)]
topOneDayByScope = [x[0] for x in sorted(topOneDayByScope, key=lambda x: x[1],reverse=True)]
topOneWeekByScope = [x[0] for x in sorted(topOneWeekByScope, key=lambda x: x[1],reverse=True)]
topSixHourByNetwork = [x[0] for x in sorted(topSixHourByNetwork, key=lambda x: x[1],reverse=True)]
topOneDayByNetwork = [x[0] for x in sorted(topOneDayByNetwork, key=lambda x: x[1],reverse=True)]
topOneWeekByNetwork = [x[0] for x in sorted(topOneWeekByNetwork, key=lambda x: x[1],reverse=True)]


outputData = {
    'emerging':emerging,
    'emergingByScope':emergingByScope,
    'emergingByNetwork':emergingByNetwork,
    'topSixHour':topSixHour,
    'topSixHourByScope':topSixHourByScope,
    'topSixHourByNetwork':topSixHourByNetwork,
    'topOneDay':topOneDay,
    'topOneDayByScope':topOneDayByScope,
    'topOneDayByNetwork':topOneDayByNetwork,
    'topOneWeek':topOneWeek,
    'topOneWeekByScope':topOneWeekByScope,
    'topOneWeekByNetwork':topOneWeekByNetwork
}




rankDirectory = './'+sys.argv[1]+'/output/ranks/'
if not os.path.exists(rankDirectory):
        os.mkdir(rankDirectory)
outputDirectory = rankDirectory+'engagementTimeSeries/'
if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)



with open(outputDirectory+'ranks.json', 'w') as outputFile:
    json.dump(outputData, outputFile,indent = 4)
