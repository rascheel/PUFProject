import os
from os.path import join, dirname, basename

import csv

from pylab import *

CSV_OUTPUT_DIR = "/home/rascheel/git/PUFProject/OutputCSVs/"
FIGURE_OUTPUT_DIR = "/home/rascheel/git/PUFProject/Figures/"

def main():
    # Walk through all the lower directories
    for root, dirs, files in os.walk(CSV_OUTPUT_DIR):
        # We only care about directories that have files
        if(len(files) != 0):
            files.sort()
            deviceName = basename(dirname(root))
            testerName = basename(root)
            print "Creating figures for device: %s, user: %s" % (deviceName, testerName)

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
                    plot(PTS, PRS, color='blue', linewidth=2, label="Pressure")
                    plot(PTS, AP, color='red', linewidth=2, linestyle="--", label="Average pressure")
                    legend(loc='upper left')
                    #show()
                    #Copy the directory structure of the OutputCSVs folder
                    deviceName = basename(dirname(root))
                    testerName = basename(root)
                    #If the directory doesn't exist make it
                    att_path = os.path.join(FIGURE_OUTPUT_DIR, deviceName, testerName)
                    if not os.path.exists(att_path):
                        os.makedirs(att_path)
                    att_path = os.path.join(att_path, fileName.split(".")[0] + ".png")
                    savefig(att_path)
                    close()


if __name__ == '__main__':
    main()
