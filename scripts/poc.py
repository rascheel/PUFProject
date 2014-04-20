from util import distBetweenPts, calcNextPt

challengeList = [(2.0,0.0), (0.0, 2.0), (-2.0,0.0), (-100.0,0), (500,500)]

challengeLength = 0.0
for i in range(0, len(challengeList)-1):
    challengeLength += distBetweenPts(challengeList[i], challengeList[i+1])
normalizedDist = challengeLength/128.0

normalizedList = []
currPt = challengeList[0]
for i in range(0, len(challengeList)-1):
    nextPt = challengeList[i+1]
    

    while(distBetweenPts(currPt, nextPt) > normalizedDist):
        normalizedList.append(currPt)
        currPt = calcNextPt(currPt, nextPt, normalizedDist)
normalizedList.append(challengeList[-1])

print normalizedList
print len(normalizedList)
