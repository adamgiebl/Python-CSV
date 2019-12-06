import matplotlib.pyplot as plt
import datetime as dt
import pprint
from fileparser import Parser



parser = Parser('data.csv')

data = parser.getData(',', '\n')

print(data)


downloadSpeeds = []
dates = []
months = []

def getAverageSpeedPerMonth(city, data):

    city = list(filter(lambda x: x['location'] == city, data)) 
    somethings = {}

    for dict in city:
        tempList = []
        month = dt.datetime.strptime(dict['date'], '%Y-%m-%d').month
        if month in somethings:
            somethings[month].append(float(dict['download']))
        else:
            tempList.append(float(dict['download']))
            somethings[month] = tempList

        downloadSpeeds.append(float(dict['download']))
        dates.append(dict['date'])

    for item in dates:
        months.append(dt.datetime.strptime(item, '%Y-%m-%d').month)

    months.sort()

    avgDict = {}
    for k,v in somethings.items():
        print(v);
        # v is the list of grades for student k
        avgDict[int(k)] = sum(v) / len(v)




    lists = sorted(avgDict.items()) 
    x, y = zip(*lists) 
    return {'x': x, 'y': y}    



dick = getAverageSpeedPerMonth('Ballerup', data)
dick2 = getAverageSpeedPerMonth('Copenhagen', data)



plt.plot(dick['x'], dick['y'], 'r', label="Bellerup")
plt.plot(dick2['x'], dick2['y'], 'b', label="Copenhagen")
plt.legend(loc='best')
plt.xticks(range(len(list(dick.keys()))))
plt.xlabel("Months")
plt.ylabel("Avg. Download speed")
plt.show()
