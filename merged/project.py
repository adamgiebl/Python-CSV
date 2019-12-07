import matplotlib.pyplot as plt
from termcolor import colored
import datetime as dt

# -----CLASS FOR PARSING-----


class Parser:
    """The class's docstring"""

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.headers = []
        self.data = []

    def getData(self, separator, lineSeparator):
        """The method's docstring"""
        file = open(self.path, encoding=self.encoding)
        txt = file.read()

        # split data into lines
        arr = txt.split(lineSeparator)

        # get headers from the first line
        self.headers = arr[0].split(separator)

        # loop over remaining lines and put them into list of dictionaries
        for line in arr[1:]:
            split = line.split(separator)

            # continue parsing only if the data is correct (same number of items as headers)
            if len(split) == len(self.headers):
                temp = []
                for i in range(len(self.headers)):
                    temp.append(split[i])
                self.data.append(dict(zip(self.headers, temp)))
        return self.data


# -----UTILITY FUNCTIONS-----

def filterByCity(city, data):
    return list(filter(lambda x: x['location'] == city, data))


def getDateObject(stringDate):
    return dt.datetime.strptime(stringDate, '%Y-%m-%d')


def getAverageFromList(list):
    # calculate the average by dividing the sum of numbers by quantity of numbers
    return sum(list) / len(list)


def getSpeedPerDates(city, data):
    city = filterByCity(city, data)
    dates = []
    speeds = []
    for dict in city:
        print(dict['download'])
        dates.append(dict['date'])
        speeds.append(float(dict['download']))

    return {'dates': dates, 'speeds': speeds}


def askUser(path):
    file = open(path, encoding='utf8')
    txt = file.read()
    print(txt)
    res = input()
    if res.isdigit():
        return int(res)
    else:
        return res.lower()


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


# -----EXECUTION-----

parser = Parser('data.csv', 'utf8')

data = parser.getData(separator=',', lineSeparator='\n')

choice = askUser('menu.txt')

while choice != 'q':
    if choice == 1:
        print(colored('CSV successfully parsed', 'green'))
        input()
    elif choice == 2:
        cityData = filterByCity('Fanø', data)
        augustAvg = getAvgSpeedInMonth('August', cityData)
        septemberAvg = getAvgSpeedInMonth('September', cityData)
        print('Average download speed for the months of August and September in Fanø is:')
        print(colored((augustAvg + septemberAvg) / 2, 'green'))
        input()
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
    choice = askUser('menu.txt')
