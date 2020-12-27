import time

from F1Classes import *

### Program Start
### Indexes
dataIndex = 'F1RemixedData.csv'
resultsIndex = 'results.txt'
breakdownIndex = 'BreakdownBySeasonLength.csv'

raceLocations2020 = ['AUT', 'STY', 'HUN', 'GBR', '70A', 'ESP', 'BEL', 'ITA', 'TUS', 'RUS', 'EIF', 'POR', 'EMI', 'TUR', 'BHR', 'SAK', 'UAE']
raceLocations2019 = ['AUS', 'BHR', 'CHN', 'AZE', 'ESP', 'MON', 'CAN', 'FRA', 'AUT', 'GBR', 'GER', 'HUN', 'BEL', 'ITA', 'SGP', 'RUS', 'JAP', 'MEX', 'USA', 'BRA', 'UAE']
raceLocations = []

### User input loop
while True:
    year = input('Select year of data to analyze (2019, 2020): ')

    if year == '2019' or year == '2020':
        dataIndex = year + dataIndex
        resultsIndex = year + resultsIndex
        breakdownIndex = year + breakdownIndex
        if year == '2020':
            raceLocations = raceLocations2020
        elif year == '2019':
            raceLocations = raceLocations2019
        break
    else:
        print('Invalid Year\n')

### Analysis Start
start = time.time()
print('Starting Analysis...')
spreadsheetData = open(dataIndex)

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
    rowIndex += 1

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

### Add each combination of races (season) to the list of seasons
for x in range(len(races)):
    xLengthSeasons = list(combinations(races, x + 1))

    for combo in xLengthSeasons:
        seasons.append(Season(drivers, list(combo)))

print('Total # of seasons: ' + str(len(seasons)))

### Do calculations on each season
print('Starting Databasing')
database = SeasonDB(seasons, drivers, resultsIndex, breakdownIndex)

print('Time: ' + str((time.time() - start) / 60))

### Program Loop
while True:
    ### Input selection
    userInput = input('\nWhat type of breakdown would you like to see?\n[t] - Percentages of all possible seasons\n[b] - Breakdown by differing season lengths\n[d] - Breakdown by driver and season length\n[q] - exit\n').lower().rstrip()

    ### Database functions
    if userInput == 't':
        # database.printResults()
        database.printResultsToFile(resultsIndex)
        print('\nResults can be found in \'' + resultsIndex + '\'')
    elif userInput == 'b':
        database.fullLengthBreakdown(len(races))
        print('\nFull percentage breakdown by season can be found in \'' + breakdownIndex + '\'')
    elif userInput == 'd':
        inputName = input('\nWhat driver would you like to breakdown?: ')
        inputLength = input('What length of season would you like to look at?: ')
        if inputLength == '':
            inputLength = '0'
        
        database.breakdownByDriverOneLength(inputName, int(inputLength), raceLocations)
    elif userInput == 'q' or userInput == 'e':
        break
    else:
        print('Not a valid input')


# ### Output
# print('Printing Results \n')
# database.printResults()
# database.printResultsToFile('results.txt')


# print()
# database.breakdownByOneLength(9)
# database.fullLengthBreakdown(len(races))