import time

from F1Classes import *

### Program Start
start = time.time()
print('Starting Analysis...')
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
for x in range(len(races)):
    xLengthSeasons = list(combinations(races, x + 1))   # list of tuples

    for combo in xLengthSeasons:
        seasons.append(Season(drivers, list(combo)))

print('Total # of seasons: ' + str(len(seasons)))

### Do calculations on each season
print('Starting Databasing')
database = SeasonDB(seasons, drivers)

### Program Loop
while True:
    userInput = input('What type of breakdown would you like to see?\n[t] - Percentages of all possible seasons\n[b] - Breakdown by differing season lengths\n[q] - exit\n').lower().rstrip()

    if userInput == 't':
        database.printResults()
        database.printResultsToFile('results.txt')
        print('Results can be found in \'results.txt\'')
    elif userInput == 'b':
        database.fullLengthBreakdown(len(races))
        print('Full percentage breakdown by season can be found in \'BreakdownBySeasonLength.csv\'')
    elif userInput == 'q' or userInput == 'e':
        break
    else:
        print('Not a valid input')


# ### Output
# print('Printing Results \n')
# database.printResults()
# database.printResultsToFile('results.txt')

# print('\nTime: ' + str((time.time() - start) / 60))

# print()
# database.breakdownByOneLength(9)
# database.fullLengthBreakdown(len(races))