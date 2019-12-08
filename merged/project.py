import matplotlib.pyplot as plt
from termcolor import colored
import datetime as dt
from console_progressbar import ProgressBar
from timeloop import Timeloop
import time

# -----CLASS FOR PARSING-----

tl = Timeloop()
progress = 0    


class Parser:

    def __init__(self, path, encoding='utf8'):
        self.path = path
        self.encoding = encoding
        self.headers = []
        self.data = []

    def getData(self, separator, lineSeparator):
        """The method's docstring"""
        finished = False
        t = time.process_time()
        """
        @tl.job(interval=dt.timedelta(seconds=0.01))
        def sample_job_every_2s():
            if not finished:
                global progress
                progress += 1
                pb.print_progress_bar(progress)
        
        tl.start()
        sample_job_every_2s()
        time.sleep(0.1)"""

        txt = ""
        with open(self.path, encoding=self.encoding) as file:
            txt = file.read()

        time_read = round(time.process_time() - t, 6)

        # split data into lines
        arr = txt.split(lineSeparator)

        # get headers from the first line
        self.headers = arr[0].split(separator)
        
        # loop over remaining lines and put them into list of dictionaries
        for line in arr[1:]:
            split = line.split(separator)

            # continue parsing only if the data is correct
            # (same number of items as headers)
            if len(split) == len(self.headers):
                temp = []
                for i in range(len(self.headers)):
                    temp.append(split[i])
                self.data.append(dict(zip(self.headers, temp)))
        time_parse = round(time.process_time() - t, 5)
        print(colored('CSV successfully parsed', 'green'))
        print(colored(f'Time to read: {time_read}s', 'white'))
        print(colored(f'Time to parse: {time_parse}s', 'yellow'))
        return self.data


# -----UTILITY FUNCTIONS-----

def filterByCity(city, data):
    return list(filter(lambda x: x['location'] == city, data))


def getDateObject(stringDate):
    return dt.datetime.strptime(stringDate, '%Y-%m-%d')


def getAverageFromList(list):
    # calculate the average by dividing the sum of numbers by quantity
    return sum(list) / len(list)


def getSpeedsPerDate(data):
    dates = []
    speeds = []
    for dict in data:
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


def getAverageSpeedPerMonths(city, data):
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


def getAvgSpeedPerMonth(selectedMonth, data):
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


def getPlotConfig(label_x="x", label_y="y", ticks=10):
    if darkMode:
        plt.style.use('dark_background')
    else:
        plt.style.use('ggplot')
    plt.tight_layout()
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.xticks(ticks)
    plt.legend(loc='best')
    plt.show()


# -----EXECUTION-----

pb = ProgressBar(total=10, prefix='Here', suffix='Now', decimals=1, length=10, fill='X', zfill='-')

parser = Parser('data.csv', 'utf8')

data = []

choice = askUser('menu.txt')

darkMode = False


while choice != 'q':
    if choice == 1:
        data = parser.getData(separator=',', lineSeparator='\n')
        input("Click ENTER to continue...")
    elif choice == 2:
        cityData = filterByCity('Fanø', data)
        augustAvg = getAvgSpeedPerMonth('August', cityData)
        septemberAvg = getAvgSpeedPerMonth('September', cityData)
        print('Average download speed for August and September in Fanø is:')
        print(colored(getAverageFromList([augustAvg, septemberAvg]), 'green'))
        input("Click ENTER to continue...")
    elif choice == 3:
        average_speed_ballerup = getAverageSpeedPerMonths('Ballerup', data)
        average_speed_copenhagen = getAverageSpeedPerMonths('Copenhagen', data)
        plt.plot(
            average_speed_ballerup['x'],
            average_speed_ballerup['y'],
            'red',
            label="Bellerup"
        )
        plt.plot(
            average_speed_copenhagen['x'],
            average_speed_copenhagen['y'],
            'blue',
            label="Copenhagen"
        )
        getPlotConfig(
            label_x="Month",
            label_y="Avg. Download speed",
            ticks=range(len(list(average_speed_ballerup['x']))+1)
        )
    elif choice == 4:
        average_speed_lolland = getAverageSpeedPerMonths('Lolland', data)
        plt.bar(
            average_speed_lolland['x'],
            average_speed_lolland['y'],
            label="Lolland"
        )
        getPlotConfig(
            label_x="Month",
            label_y="Avg. Download speed",
            ticks=range(len(list(average_speed_lolland['x']))+1)
        )
    elif choice == 5:
        darkMode ^= True
        print("Dark mode is: ", end=" ")
        if darkMode:
            print(colored("ON", "green"))
        else:
            print(colored("OFF", "red"))
        input("Click ENTER to continue...")
    choice = askUser('menu.txt')
