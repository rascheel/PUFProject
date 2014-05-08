import math
from scipy.stats import norm
from util import interpolatedPressure, getRawDataLists, meanAndStdDev, testPressListVsDistrib, genMeanList, genGraph


def main():
    allowedDeviation = 3

    dataLists = getRawDataLists()
    filteredLists = filter(lambda dataList: dataList.seed == 2003 and 
                                            dataList.testerName == "Ryan" and 
                                            dataList.deviceName == "nexus-06", 
                           dataLists)
    
    interpPressLists = []
    for dataList in filteredLists:
        interpPressLists.append(interpolatedPressure(n=32, dataList=dataList))

    tmpLists = []
    for i in range(0,32):
        distrib = []
        for interpPressList in interpPressLists:
            distrib.append(interpPressList[i])
        tmpLists.append(distrib)
    
    interpPressDistribs = []
    for distrib in tmpLists:
        interpPressDistribs.append(meanAndStdDev(distrib))

    for distrib in interpPressDistribs:
        print distrib

    for i in range(0, len(interpPressLists)):
        print "Failed Points = %d : %s" % (testPressListVsDistrib(interpPressLists[i],
                                                                  interpPressDistribs,
                                                                  allowedDeviation),
                                           filteredLists[i].fileName)
        xArray = range(0,32)
        yArrays = []
        yLabels = []

        yArrays.append(genMeanList(interpPressDistribs, 0.0))
        yLabels.append("Mean pressure")

        yArrays.append(genMeanList(interpPressDistribs, allowedDeviation))
        yLabels.append("Mean pressure + %.1f deviations" % allowedDeviation)

        yArrays.append(genMeanList(interpPressDistribs, -allowedDeviation))
        yLabels.append("Mean pressure - %.1f deviations" % allowedDeviation)

        yArrays.append(interpPressLists[i])
        yLabels.append("Interpolated Response")

        #genGraph(xArray, yArrays, yLabels, xLabel="Points", yLabel="Pressure",
        #         graphTitle=filteredLists[i].fileName)








   







if __name__ == '__main__':
    main()
