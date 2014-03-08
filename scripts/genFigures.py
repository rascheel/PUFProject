import os
from os.path import join, dirname, basename

import csv
from util import simpleMovingAverage, cumulativeMovingAverage

from pylab import *

CSV_OUTPUT_DIR = "/home/rascheel/git/PUFProject/OutputCSVs/"
COMBINED_FIGURE_OUTPUT_DIR = "/home/rascheel/git/PUFProject/Figures/Combined"
INDIVIDUAL_FIGURE_OUTPUT_DIR = "/home/rascheel/git/PUFProject/Figures/Individual"

def main():
    genIndividualFigures()
    genCombinedFigures()

def genIndividualFigures():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()
            deviceName = basename(dirname(root))
            testerName = basename(root)
            print "Creating individual figures for device: %s, user: %s" % (deviceName, testerName)

            # The directories with files have the .csv files
            # Get the pressure data from them and store in list
            for fileName in files:
                with open(join(root, fileName), "rb") as csvfile:
                    respReader = csv.reader(csvfile)
                    dataStarted = False
                    challengeX = []
                    challengeY = []
                    testerName = ""
                    deviceName = ""
                    pathSeed = fileName.split(":")[0]
                    respX= []
                    respY= []
                    pressureList = []
                    for row in respReader:
                        if(dataStarted):
                            respX.append(float(row[0]))
                            respY.append(float(row[1]))
                            pressureList.append(float(row[2]))
                        elif(row[0] != "ChallengeX" and row[0] != "X"):
                            challengeX.append(float(row[0]))
                            challengeY.append(float(row[1]))
                            testerName = row[2]
                            deviceName = row[3]

                        if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                            dataStarted = True

                    #Calculate average pressure
                    avgPres = 0
                    for pres in pressureList:
                        avgPres = avgPres + pres
                    avgPres = avgPres / len(pressureList)

                    #Calculate simple moving average n = 5
                    movingAvg5 = simpleMovingAverage(pressureList, 5)

                    #Calculate simple moving average n = 10
                    movingAvg10 = simpleMovingAverage(pressureList, 10)

                    #Calculate cumulative moving average
                    cumulativeMovAvg = cumulativeMovingAverage(pressureList)

                    #Create figure to graph with
                    fig = figure(figsize=(16,12))
                    fig.suptitle("Path: %s\n Device: %s\n User: %s" % (pathSeed, deviceName, testerName))
                    #Setup plot of path traced
                    subplot(1,2,1)
                    xlim(0,800)
                    ylim(1280,0)
                    title("Challenge/Response Path")
                    xlabel("X location (pixels)")
                    ylabel("Y location (pixels)")
                    CX = np.array(challengeX)
                    CY = np.array(challengeY)
                    plot(CX, CY, color='green', linewidth=2, linestyle="--", label="Generated Challenge")
                    RX = np.array(respX)
                    RY = np.array(respY)
                    plot(RX, RY, color='blue', linewidth=2, label="User Response")
                    annotate("Start", xy=(challengeX[0], challengeY[0]), bbox=dict(facecolor='white', edgecolor='None', alpha=0.65 ))
                    annotate("End", xy=(challengeX[-1], challengeY[-1]), bbox=dict(facecolor='white', edgecolor='None', alpha=0.65 ))
                    legend(loc='upper left')
                    #Setup plot of pressure data
                    subplot(1,2,2)
                    title("Recorded Pressure")
                    xlabel("Points")
                    ylabel("Pressure")
                    ylim(0, 1.0)
                    PTS = np.linspace(1,len(pressureList), len(pressureList))
                    PRS = np.array(pressureList)
                    AP = np.linspace(avgPres, avgPres, len(pressureList))
                    MA5 = np.array(movingAvg5)
                    MA10 = np.array(movingAvg10)
                    CMA = np.array(cumulativeMovAvg)
                    plot(PTS, PRS, color='blue', linewidth=2, label="Pressure")
                    plot(PTS, AP, color='black', linewidth=2, linestyle="--", label="Average pressure")
                    plot(PTS, MA5, color='red', linewidth=2, linestyle="-", label="Moving average n = 5")
                    plot(PTS, MA10, color='cyan', linewidth=2, linestyle="-", label="Moving average n = 10")
                    plot(PTS, CMA, color='magenta', linewidth=2, linestyle="-", label="Cumulative moving average")
                    legend(loc='lower right')
                    #Copy the directory structure of the OutputCSVs folder
                    deviceName = basename(dirname(root))
                    testerName = basename(root)
                    #If the directory doesn't exist make it
                    att_path = os.path.join(INDIVIDUAL_FIGURE_OUTPUT_DIR, deviceName, testerName)
                    if not os.path.exists(att_path):
                        os.makedirs(att_path)
                    att_path = os.path.join(att_path, fileName.split(".")[0] + ".png")
                    #NOTE: Cannot show and save figure at same time
                    #show()
                    savefig(att_path)
                    close()

def genCombinedFigures():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()
            deviceName = basename(dirname(root))
            testerName = basename(root)
            print "Creating combined figures for device: %s, user: %s" % (deviceName, testerName)

            # The directories with files have the .csv files
            # Get the pressure data from them and store in list
            challengeX = []
            challengeY = []
            respX= []
            respY= []
            pressureList = []
            pathSeed = []
            count = 0
            for fileName in files:
                count += 1
                pathSeed.append(fileName.split(":")[0])
                with open(join(root, fileName), "rb") as csvfile:
                    respReader = csv.reader(csvfile)
                    dataStarted = False
                    for row in respReader:
                        if(dataStarted):
                            respX.append(float(row[0]))
                            respY.append(float(row[1]))
                            pressureList.append(float(row[2]))
                        elif(row[0] != "ChallengeX" and row[0] != "X"):
                            challengeX.append(float(row[0]))
                            challengeY.append(float(row[1]))
                            testerName = row[2]
                            deviceName = row[3]

                        if(row[0] == "X" and row[1] == "Y" and row[2] == "PRESSURE"):
                            dataStarted = True

                    if count == 10:#len(files):
                        #Calculate average pressure
                        avgPres = 0
                        for pres in pressureList:
                            avgPres = avgPres + pres
                        avgPres = avgPres / len(pressureList)

                        #Calculate simple moving average n = 5
                        movingAvg5 = simpleMovingAverage(pressureList, 5)

                        #Calculate simple moving average n = 10
                        movingAvg10 = simpleMovingAverage(pressureList, 10)

                        #Calculate cumulative moving average
                        cumulativeMovAvg = cumulativeMovingAverage(pressureList)

                        #Create figure to graph with
                        fig = figure(figsize=(16,12))
                        fig.suptitle("Combined Paths: %s\n Device: %s\n User: %s" % (",".join(pathSeed),deviceName, testerName))
                        #Setup plot of pressure data with averages
                        title("Recorded Pressure")
                        xlabel("Points")
                        ylabel("Pressure")
                        ylim(0, 1.0)
                        PTS = np.linspace(1,len(pressureList), len(pressureList))
                        PRS = np.array(pressureList)
                        AP = np.linspace(avgPres, avgPres, len(pressureList))
                        MA5 = np.array(movingAvg5)
                        MA10 = np.array(movingAvg10)
                        CMA = np.array(cumulativeMovAvg)
                        plot(PTS, PRS, color='blue', linewidth=2, label="Pressure")
                        plot(PTS, AP, color='black', linewidth=2, linestyle="--", label="Average pressure")
                        plot(PTS, MA5, color='red', linewidth=2, linestyle="-", label="Moving average n = 5")
                        plot(PTS, MA10, color='cyan', linewidth=2, linestyle="-", label="Moving average n = 10")
                        plot(PTS, CMA, color='magenta', linewidth=2, linestyle="-", label="Cumulative moving average")
                        legend(loc='lower right')
                        #Copy the directory structure of the OutputCSVs folder
                        deviceName = basename(dirname(root))
                        testerName = basename(root)
                        #If the directory doesn't exist make it
                        att_path = os.path.join(COMBINED_FIGURE_OUTPUT_DIR, deviceName, testerName)
                        if not os.path.exists(att_path):
                            os.makedirs(att_path)
                        att_path = os.path.join(att_path, "Combined Paths: %s; Device: %s; User: %s" % (",".join(pathSeed),deviceName, testerName))
                        #NOTE: Cannot show() and savefig() at same time
                        #show()
                        savefig(att_path)
                        #Close figure to cleanup memory
                        close()
                        #clear lists
                        challengeX = []
                        challengeY = []
                        respX= []
                        respY= []
                        pathSeed = []
                        pressureList = []
                        count = 0

if __name__ == '__main__':
    main()
