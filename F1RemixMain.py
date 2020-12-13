import csv
from itertools import combinations
# import pandas as pd
# from operator import itemgetter

"""
Classes needed:
    Race
    Driver
"""

class Driver:
    def __init__(self, name):
        self.name = name
        self.pointsArray = []

    def printDriver(self):
        print(self.name, end='')
        for finish in self.pointsArray:
            print(', ' + str(finish), end='')
        print()

    def getPointsFromRaceIndex(self, index):
        return pointsArray[index]

class Race:
    def __init__(self, calendarPosition):
        self.calendarPosition = calendarPosition
        self.finisherNames = []

    def printRaceResults(self):
        print('Race ' + str(self.calendarPosition) + ':', end=' ')
        for finisher in self.finisherNames:
            print(finisher + ', ', end='')
        print()

class Season:
    def __init__(self, drivers, races):
        self.races = []
        self.champ = ''
        self.standings = []
        self.drivers = drivers.copy()
        self.driverPoints = []
    
    def importStandingsPoints(self, drivers):
        for race in races:
            for finisher in race.finisherNames:
                for driver in drivers.name:
                    if finisher == driver:
                        driverPointsTotal = driver.getPointsFromRaceIndex(race.calendarposition)
                        i = 0
                        for names in driverPoints:
                            if names[0] == driver.name:
                                driverPoints[i] += driverPointsTotal
                                break
                            i += 1
                        driverPoints.append((driver, driverPointsTotal))

                        


spreadsheetData = open("ChrisFuchsData.csv")

#print(spreadsheetData.readlines())

### Arrays
races = []
drivers = []

### Import driver finishes from spreadsheet
rowIndex = 0

for row in spreadsheetData.readlines():
    if rowIndex > 0:
        driverData = row.split(",")
        #print(driverData)
        driverObject = Driver(driverData[1])
        for finish in driverData[2:-1]:
            #print(finish)
            driverObject.pointsArray.append(float(finish))
        drivers.append(driverObject)
        del driverObject
    rowIndex = rowIndex + 1

spreadsheetData.seek(0)

for event in range(len(spreadsheetData.readline().split(',')) - 3):
    raceObject = Race(event)

    ### Import finishing orders from the drivers objects
    finishingOrder = []
    for driver in drivers:
        finishingOrder.append(driver.pointsArray[event])

    finishingOrder.sort(reverse=True)
    midstep = []
    deletableDrivers = drivers.copy()

    for points in finishingOrder:
        for driver in deletableDrivers:
            if points == driver.pointsArray[event]:
                midstep.append(driver.name)
                deletableDrivers.remove(driver)     # wait does this actually work?????
    
    raceObject.finisherNames = midstep
    races.append(raceObject)
    del raceObject
    
"""
for race in races:
    race.printRaceResults()
"""

possibleSeasonCombinations = []

for x in range(1, len(races) + 1):
    xLengthSeasons = list(combinations(races, x))

    # xLengthSeasons[0][0].printRaceResults()
    possibleSeasonCombinations.extend(xLengthSeasons)
    # break

print(len(possibleSeasonCombinations))

# print(drivers[0].name)

# for driver in drivers:
#     driver.printDriver()

# races[1].printRaceResults()

# for race in races:
#     race.printRaceResults()

#print(spreadsheetData.readlines())

# for driver in drivers:
#      driver.printDriver()

#print(drivers[1].pointsArray[1])

"""
for line in spreadsheetData.readlines():
    for col in line.split(","):
        print(col)
"""