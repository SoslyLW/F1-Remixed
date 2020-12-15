import csv
import random
from itertools import combinations
import time

### Classes
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
        return self.pointsArray[index]

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
        self.races = races
        self.champ = ''
        self.standings = []
        self.drivers = drivers
        self.driverPoints = {}

        self.initDict()
        self.importStandingsPoints()
        self.determineChamp()
    
    def initDict(self):
        for driver in drivers:
            self.driverPoints[driver.name] = 0

    def importStandingsPoints(self):
        for race in self.races:
            for finisher in race.finisherNames:
                for driver in self.drivers:
                    if finisher == driver.name:
                        driverPointsTotal = driver.getPointsFromRaceIndex(race.calendarPosition)

                        self.driverPoints[driver.name] += driverPointsTotal
    
    def determineChamp(self, highestpoints = -1):
        champName = ''

        for pointTotal in self.driverPoints.items():
            if pointTotal[1] > highestpoints:
                champName = pointTotal[0]
                highestpoints = pointTotal[1]
            elif pointTotal[1] == highestpoints:
                champName = self.tiebreak(self.findDriverByName(champName), self.findDriverByName(pointTotal[0]))

        self.champ = self.findDriverByName(champName).name

    def tiebreak(self, driver1, driver2):
        ### Note: tiebreak only accounts for top ten finishes, not any finishes
        
        driver1count = {}
        driver2count = {}
        counter = 0

        for x in range(10):
            driver1count[x] = 0
            driver2count[x] = 0

        # Find number of each finishing positions for each driver
        for finish in self.races:
            for x in range(10):
                if finish.finisherNames[x] == driver1.name:
                    driver1count[x] += 1
                
        for finish in self.races:
            for x in range(10):
                if finish.finisherNames[x] == driver2.name:
                    driver2count[x] += 1
            
        # tiebreaking section
        for i in range(len(driver1count.items())):
            if driver1count[i] > driver2count[i]:
                return driver1.name
            if driver2count[i] > driver1count[i]:
                return driver2.name

        return driver1.name + ' ' + driver2.name

    def findDriverByName(self, name):
        for driver in self.drivers:
            if name == driver.name:
                return driver

        # if no name is found (usually as a reult of a tie return two names combined)
        brokenNames = []
        twoNameNames = list(combinations(name.split(' '), 2))
        threeNameNames = list(combinations(name.split(' '), 3))

        for x in twoNameNames:
            fullName = x[0] + ' ' + x[1]
            brokenNames.append(fullName)

        for x in threeNameNames:
            fullName = x[0] + ' ' + x[1] + ' ' + x[2]
            brokenNames.append(fullName)

        random.shuffle(brokenNames)

        for comboName in brokenNames:
            for driver in self.drivers:
                if comboName.strip() == driver.name.strip():
                    return driver

        print('no driver found')
        return

class SeasonDB:
    def __init__(self, seasons, drivers):
        self.seasons = seasons
        self.drivers = drivers
        self.champDict = {}

        self.initDict()
        self.calcChampionships()

    def initDict(self):
        for driver in self.drivers:
            self.champDict[driver.name] = 0

    def calcChampionships(self):
        for season in self.seasons:
            if season.champ:
                for driver in self.drivers:
                    if season.champ == driver.name:
                        self.champDict[driver.name] += 1

    def printResults(self):
        for driver in self.champDict.items():
            print(driver[0] + ' ' + str(str(driver[1]) + ' Pct: ' + str(round(driver[1]*100.0/len(seasons), 3))))

    def printResultsToFile(self, filename):
        f = open(filename, 'w')

        for driver in self.champDict.items():
            f.write(driver[0] + ' ' + str(str(driver[1]) + ' Pct: ' + str(round(driver[1]*100.0/len(seasons), 3)) + '\n'))
        
        f.close()

start = time.time()
spreadsheetData = open("ChrisFuchsData.csv")

### Arrays
races = []
drivers = []
seasons = []

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

### Initialize every race (including sorting finishing order)
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
                deletableDrivers.remove(driver)
    
    raceObject.finisherNames = midstep
    races.append(raceObject)
    del raceObject

### Add each combinatiion of races (season) to the list of seasons
for x in range(1, len(races) + 1):
    xLengthSeasons = list(combinations(races, x))   # list of tuples

    for combo in xLengthSeasons:
        seasons.append(Season(drivers, list(combo)))

print('Total # of seasons: ' + str(len(seasons)))

### Do calculations on each season
print('Starting Databasing')
database = SeasonDB(seasons, drivers)

### Output
print('Printing Results \n')
database.printResults()
database.printResultsToFile('results.txt')

print('\nTime: ' + str((time.time() - start) / 60))