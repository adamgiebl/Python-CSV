import matplotlib.pyplot as plt
import pprint
from fileparser import Parser
from menu import askUser
from utilities import filterByCity, getDateObject, getAverageFromList

parser = Parser('data.csv')

data = parser.getData(separator=',', lineSeparator='\n')

choice = int(askUser('menu.txt'))

def getAverageSpeedPerMonth(city, data):
    downloadSpeeds = []
    dates = []
    months = []
    city = filterByCity(city, data)
    somethings = {}
    for dict in city:
        tempList = []
        month = getDateObject(dict['date']).month
        if month in somethings:
            somethings[month].append(float(dict['download']))
        else:
            tempList.append(float(dict['download']))
            somethings[month] = tempList

        downloadSpeeds.append(float(dict['download']))
        dates.append(dict['date'])

    for item in dates:
        months.append(getDateObject(item).month)

    avgDict = {}
    for k, v in somethings.items():
        avgDict[int(k)] = getAverageFromList(v)

    lists = sorted(avgDict.items())
    x, y = zip(*lists)
    return {'x': x, 'y': y}


def getAvgSpeedInMonth(selectedMonth, data):
    downloadSpeeds = []
    dates = []
    months = []
    somethings = {}

    for dict in data:
        tempList = []
        month = getDateObject(dict['date']).strftime("%B")
        if month in somethings:
            somethings[month].append(float(dict['download']))
        else:
            tempList.append(float(dict['download']))
            somethings[month] = tempList

    avgSpeed = getAverageFromList(somethings[selectedMonth])
    return avgSpeed

if choice == 2:
    cityData = filterByCity('Fanø', data)
    augustAvg = getAvgSpeedInMonth('August', cityData)
    septemberAvg = getAvgSpeedInMonth('September', cityData)
    print(f'Average download speed for the months of August and September in Fanø is {(augustAvg + septemberAvg) / 2}')
elif choice == 3:
    dick = getAverageSpeedPerMonth('Ballerup', data)
    dick2 = getAverageSpeedPerMonth('Copenhagen', data)
    plt.plot(dick['x'], dick['y'], 'r', label="Bellerup")
    plt.plot(dick2['x'], dick2['y'], 'b', label="Copenhagen")
    plt.xticks(range(len(list(dick['x']))+1))
    plt.xlabel("Months")
    plt.ylabel("Avg. Download speed")
    plt.legend(loc='best')
    plt.show()
elif choice == 4:
    dick = getAverageSpeedPerMonth('Lolland', data)
    plt.bar(dick['x'], dick['y'], label="Bellerup")
    plt.xticks(range(len(list(dick['x']))+1))
    plt.xlabel("Months")
    plt.ylabel("Avg. Download speed")
    plt.legend(loc='best')
    plt.show()

