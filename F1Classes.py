import random
import csv
import math
from itertools import combinations

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
        for driver in self.drivers:
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
    def __init__(self, seasons, drivers, resultsIndex, breakdownIndex):
        self.seasons = seasons
        self.drivers = drivers
        self.champDict = {}
        self.breakdownLengthIndex = breakdownIndex
        self.resultsIndex = resultsIndex

        self.initDict(self.champDict)
        self.calcChampionships()

    def initDict(self, dicti):
        for driver in self.drivers:
            dicti[driver.name] = 0

    def calcChampionships(self):
        for season in self.seasons:
            if season.champ:
                for driver in self.drivers:
                    if season.champ == driver.name:
                        self.champDict[driver.name] += 1

    def breakdownByOneLength(self, length):
        specificLengthSeasons = []
        specificLengthDict = {}
        self.initDict(specificLengthDict)

        for season in self.seasons:
            if len(season.races) == length:
                specificLengthSeasons.append(season)

        for season in specificLengthSeasons:
            for driver in self.drivers:
                if season.champ == driver.name:
                    specificLengthDict[driver.name] += 1

        # self.printResultsFromDict(specificLengthDict, len(specificLengthSeasons))
        return specificLengthDict
        

    def fullLengthBreakdown(self, seasonLength):
        print('Running Breakdown by Season Length')

        topRow = ['Driver']
        csvList = []
        driverLists = []

        for x in range(seasonLength):
            csvList.append(self.breakdownByOneLength(x + 1))
            topRow.append(str(x + 1))

        for x in self.drivers:
            driverLists.append([x.name])
        
        i = 1
        for dicti in csvList:
            for driver in dicti.items():
                for person in driverLists:
                    if person[0] == driver[0]:
                        person.append(round(driver[1] / math.comb(seasonLength, i) * 100, 3))
            i += 1
        
        with open(self.breakdownLengthIndex, 'w', newline='') as f:
            w = csv.writer(f, delimiter=',')

            w.writerow(topRow)
            w.writerows(driverLists)

    def breakdownByDriverOneLength(self, name, length, raceLocations):
        racesInWinningSeason = []

        for season in self.seasons:
            if len(season.races) == int(length):
                if season.champ.lower().rstrip() == name.lower().rstrip():
                    racePositions = []
                    for race in season.races:
                        if raceLocations:
                            racePositions.append(raceLocations[race.calendarPosition])
                        else:
                            racePositions.append(race.calendarPosition)
                    
                    racesInWinningSeason.append(racePositions)

        if not racesInWinningSeason:
            print('Invalid driver name or length (Hint: Carlos Sainz Jr. may be an issue)')
            return
        
        print(name + 'wins the WDC in the following seasons:')
        print(racesInWinningSeason)

    def printResults(self):
        for driver in self.champDict.items():
            print(driver[0] + ' ' + str(str(driver[1]) + ' Pct: ' + str(round(driver[1]*100.0/len(self.seasons), 3))))

    def printResultsToFile(self, filename):
        f = open(filename, 'w')

        for driver in self.champDict.items():
            f.write(driver[0] + ' ' + str(str(driver[1]) + ' Pct: ' + str(round(driver[1]*100.0/len(self.seasons), 3)) + '\n'))
        
        f.close()

    def printResultsFromDict(self, dicti, length):
        for driver in dicti.items():
            print(driver[0] + ' ' + str(str(driver[1]) + ' Pct: ' + str(round(driver[1]*100.0/length, 3))))

    def printSeasonCSV(self, f):
        for row in f.readlines():
            if type(row) == list:
                for col in row.spilt(','):
                    print(col)