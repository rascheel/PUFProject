import csv
import os.path
from os import listdir

def main():

    # TODO: at some point make this not hard coded
    csvFilePath = "/home/rascheel/git/PUFProject/OutputCSVs/nexus-03/Jake/"

    fileList = listdir(csvFilePath)
    fileList.sort()
    #print fileList

    pressureList = []

    for fileName in fileList:
        with open(csvFilePath + fileName, "rb") as csvfile:
            respReader = csv.reader(csvfile)
            dataStarted = False
            for row in respReader:
                if(dataStarted):
                    pressureList.append(float(row[2]))
                if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                    dataStarted = True

    count = 0
    bitString = ""
    for i in range(0, len(pressureList)-1):
        if(pressureList[i] != pressureList[i+1]):
            bitString += str(arbiter(pressureList[i], pressureList[i+1]))
            count += 1

    #print bitString
    #print "PressureList Length: " + str(len(pressureList))
    #print "Bit Count: " + str(count)
    #print pressureList


    # TODO: at some point make this not hard coded
    outputFilePath = "/home/rascheel/git/PUFProject/OutputGenerated/Strat1/"
    with open(outputFilePath + "resp1", "wb") as outputFile:
        outputFile.write(bitString)

def arbiter(val1, val2):
    return 0 if val1 < val2 else 1 #ternary operation

if __name__ == '__main__':
    main()
