import binascii
from math import sqrt, atan, sin, cos, fabs
from pylab import *

def hammingDistance(byteArr1, byteArr2):
    if(len(byteArr1) != len(byteArr2)):
        raise ValueError("Undefined for sequences of unequal length")

    hammDist = 0
    for i in range(0, len(byteArr1)):
        for j in range(0, 8):
            bit1 = byteArr1[i] & (1 << j)
            bit2 = byteArr2[i] & (1 << j)
            if( bit1 != bit2 ):
                hammDist += 1

    return hammDist

def simpleMovingAverage(inputList, n=5):
    returnList = []
    for i in range(0, len(inputList)):
        floor = i-n/2
        if floor < 0:
            floor = 0
        if n%2 == 1:
            spliceList = inputList[floor:(i+n/2+1)]
            returnList.append(sum(spliceList, dtype="float")/float(len(spliceList)))
        else:
            spliceList = inputList[floor:(i+n/2)]
            returnList.append(sum(spliceList, dtype="float")/float(len(spliceList)))
    return returnList

def cumulativeMovingAverage(inputList):
    cumulativeMovAvg = []
    for i in range(0, len(inputList)):
        if i == 0:
            cumulativeMovAvg.append(float(inputList[0]))
        else:
            cumulAvg = (cumulativeMovAvg[i-1]*float(i-1) + float(inputList[i]))/float(i)
            cumulativeMovAvg.append(cumulAvg)
    return cumulativeMovAvg

def distBetweenPts(pt1=(0,0), pt2=(0,0)):
    return sqrt(pow(pt1[0]-pt2[0], 2) + pow(pt1[1]-pt2[1], 2))

def calcNextPt(lastPt=(0,0), targetPt=(0,0), increment=0):
    if(lastPt[1] > targetPt[1]):
        increment = -increment

    deltaX = 0
    deltaY = 0
    if(lastPt[1] == targetPt[1]): #tan(X/0) is NaN
        if(lastPt[0] > targetPt[0]):
            deltaX = -increment
        else:
            deltax = increment
    else:
        angle = atan((lastPt[0]-targetPt[0])/(lastPt[1]-targetPt[1]))
        deltaX = increment * sin(angle)
        deltaY = increment * cos(angle)

    nextPt = (lastPt[0]+deltaX, lastPt[1]+deltaY)
    return nextPt
