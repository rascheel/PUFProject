import os
from os.path import join, dirname, basename

from util import simpleMovingAverage, cumulativeMovingAverage

import csv

CSV_OUTPUT_DIR = "/home/rascheel/git/PUFProject/OutputCSVs/"
GENERATED_OUTPUT_DIR = "/home/rascheel/git/PUFProject/OutputGenerated/"

def main():
    Strat1()
    Strat2()
    Strat3()
    Strat4()

def Strat1():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()

            # The directories with files have the .csv files
            # Get the pressure data from them and store in list
            pressureList = []
            for fileName in files:
                with open(join(root, fileName), "rb") as csvfile:
                    respReader = csv.reader(csvfile)
                    dataStarted = False
                    for row in respReader:
                        if(dataStarted):
                            pressureList.append(float(row[2]))
                        if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                            dataStarted = True

            #Determine global variable average pressure for use in the arbiter
            for pressure in pressureList:
                averagePressure = averagePressure + pressure
            averagePressure = averagePressure / len(pressureList)

            #Build the bit string and convert it to a bytearray() type for writing 
            #to a binary file
            bitString = ""
            for i in range(0, len(pressureList)-1):
                bitString += str(arbiter(pressureList[i], averagePressure))
            byteArr = convBitStrToByteArr(bitString)

            #Copy the directory structure of the OutputCSVs folder
            deviceName = basename(dirname(root))
            testerName = basename(root)

            #If the directory doesn't exist make it
            att_path = os.path.join(GENERATED_OUTPUT_DIR, "Strat1", deviceName, testerName, "responseBinary")
            if not os.path.exists(att_path):
                os.makedirs(os.path.dirname(att_path))

            #Write binary file
            with open(att_path, "wb") as outputFile:
                outputFile.write(byteArr)


def Strat2():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()

            # The directories with files have the .csv files
            # Get the pressure data from them and store in list
            pressureList = []
            for fileName in files:
                with open(join(root, fileName), "rb") as csvfile:
                    respReader = csv.reader(csvfile)
                    dataStarted = False
                    for row in respReader:
                        if(dataStarted):
                            pressureList.append(float(row[2]))
                        if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                            dataStarted = True

            #Calculate moving average n = 5 for use in arbiter
            movingAvg5 = simpleMovingAverage(pressureList, 5)

            #Build the bit string and convert it to a bytearray() type for writing 
            #to a binary file
            bitString = ""
            for i in range(0, len(pressureList)):
                bitString += str(arbiter(pressureList[i], movingAvg5[i]))
            byteArr = convBitStrToByteArr(bitString)

            #Copy the directory structure of the OutputCSVs folder
            deviceName = basename(dirname(root))
            testerName = basename(root)

            #If the directory doesn't exist make it
            att_path = os.path.join(GENERATED_OUTPUT_DIR, "Strat2", deviceName, testerName, "responseBinary")
            if not os.path.exists(att_path):
                os.makedirs(os.path.dirname(att_path))

            #Write binary file
            with open(att_path, "wb") as outputFile:
                outputFile.write(byteArr)

def Strat3():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()

            # The directories with files have the .csv files
            # Get the pressure data from them and store in list
            pressureList = []
            for fileName in files:
                with open(join(root, fileName), "rb") as csvfile:
                    respReader = csv.reader(csvfile)
                    dataStarted = False
                    for row in respReader:
                        if(dataStarted):
                            pressureList.append(float(row[2]))
                        if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                            dataStarted = True

            #Calculate moving average n = 5 for use in arbiter
            movingAvg10 = simpleMovingAverage(pressureList, 10)

            #Build the bit string and convert it to a bytearray() type for writing 
            #to a binary file
            bitString = ""
            for i in range(0, len(pressureList)):
                bitString += str(arbiter(pressureList[i], movingAvg10[i]))
            byteArr = convBitStrToByteArr(bitString)

            #Copy the directory structure of the OutputCSVs folder
            deviceName = basename(dirname(root))
            testerName = basename(root)

            #If the directory doesn't exist make it
            att_path = os.path.join(GENERATED_OUTPUT_DIR, "Strat3", deviceName, testerName, "responseBinary")
            if not os.path.exists(att_path):
                os.makedirs(os.path.dirname(att_path))

            #Write binary file
            with open(att_path, "wb") as outputFile:
                outputFile.write(byteArr)

def Strat4():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()

            # The directories with files have the .csv files
            # Get the pressure data from them and store in list
            pressureList = []
            for fileName in files:
                with open(join(root, fileName), "rb") as csvfile:
                    respReader = csv.reader(csvfile)
                    dataStarted = False
                    for row in respReader:
                        if(dataStarted):
                            pressureList.append(float(row[2]))
                        if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                            dataStarted = True

            #Calculate cumulative moving average
            cumulativeMovAvg = []
            for i in range(0, len(pressureList)):
                cumulativeMovAvg.append(sum(pressureList[0:i+1], dtype='float')/len(pressureList[0:i+1]))

            #Build the bit string and convert it to a bytearray() type for writing 
            #to a binary file
            bitString = ""
            for i in range(0, len(pressureList)):
                bitString += str(arbiter(pressureList[i], cumulativeMovAvg[i]))
            byteArr = convBitStrToByteArr(bitString)

            #Copy the directory structure of the OutputCSVs folder
            deviceName = basename(dirname(root))
            testerName = basename(root)

            #If the directory doesn't exist make it
            att_path = os.path.join(GENERATED_OUTPUT_DIR, "Strat4", deviceName, testerName, "responseBinary")
            if not os.path.exists(att_path):
                os.makedirs(os.path.dirname(att_path))

            #Write binary file
            with open(att_path, "wb") as outputFile:
                outputFile.write(byteArr)

def arbiter(val1, val2):
    return 0 if val1 > val2 else 1 #ternary operation

def convBitStrToByteArr(bitString):

    byteToBuild = 0

    #Chop up the bitstring into a list of 8-length strings
    byteList = [bitString[i:i+8] for i in range(0, len(bitString), 8)]

    byteArr = bytearray()
    for byteStr in byteList:
        for i in range(0,8):
            if i < len(byteStr):
                byteToBuild = byteToBuild | (int(byteStr[i]) << (7-i))
        byteArr.append(byteToBuild)
        byteToBuild = 0

    return byteArr

        

if __name__ == '__main__':
    main()
