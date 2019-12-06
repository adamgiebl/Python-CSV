import datetime as dt

def filterByCity(city, data):
    return list(filter(lambda x: x['location'] == city, data)) 

def getDateObject(stringDate):
    return dt.datetime.strptime(stringDate, '%Y-%m-%d')

def getAverageFromList(list):
    #calculate the average by dividing the sum of numbers by quantity of numbers 
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