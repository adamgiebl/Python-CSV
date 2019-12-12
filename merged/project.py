import matplotlib.pyplot as plt
from termcolor import colored
from os import path
import datetime as dt
from time import process_time
import csv
import colorama
from pprint import pprint as pp



class Parser:
    """This is a class for parsing and retrieving CSV data."""

    def __init__(self, encoding='utf8'):
        """
        Args:
            encoding (str, optional): Specify which encoding should be used in
                reading the file.
        """
        self.encoding = encoding

    def get_path():
        """Method that asks a user for a path and returns it.

        Provides simple validation if file doesn't exists or user has put in a 
        file that is not a csv.

        Returns:
            String if successful, None otherwise.
        """
        path_csv = input('Enter path to your csv file: ')
        if path.exists(path_csv):
            extension = path.splitext(path_csv)[1]
            if extension == '.csv':
                return path_csv
            else:
                print(colored('File is not a csv', 'red'))
                return None
        else:
            print(colored('File doesn\'t exist', 'red'))
            return None

    def get_data(self, separator):
        """Method for reading csv contents and parsing it into a list of
            dictionaries.

        Uses the csv module. Method can handle data with x amount of columns
        and will automatically assign correct headers.

        Args:
            separator (str): Defines how are values separated in a csv file.

        Returns:
            List of ditionaries if successful, None otherwise.
        """
        path_csv = self.get_path()
        if path_csv is None:
            return

        # start counting time elapsed
        t = process_time()

        data = []

        with open(path_csv, encoding=self.encoding) as file:

            reader = csv.reader(file, delimiter=separator)

            # get headers from the first line
            headers = next(reader)

            # loop over remaining lines and put them into list of dictionaries
            for line in reader:
                # continue parsing only if the data is correct
                # (same number of items as headers)
                if len(line) == len(headers):
                    values = []
                    for i in range(len(headers)):
                        values.append(line[i])
                    # connecting values with headers and creating a dictionary
                    data.append(dict(zip(headers, values)))

        # getting result of time elapsed
        time_elapsed = round(process_time() - t, 5)

        print(colored('CSV successfully parsed with csv module', 'green'))
        print(colored(f'Time to read and parse: {time_elapsed}s', 'white'))

        return data


def check_data(func):
    """Decorator function to check if the data exists before user tries to use functions that require it."""
    def inner(*args, **kwargs):
        # checking if first argument (data) is empty
        if args[0]:
            func(*args, **kwargs)
        else:
            print(colored("There is not data to work with.", 'red'))
            print("Try parsing the file first.")
            input("Click ENTER to continue...")
    return inner


def filter_by_city(city, data):
    """Filters data by city name.

    Args:
        city (str): City name.
        data (list of dict): Data to be filtered.

    Returns:
        list: List of ditionaries.
    """
    # filter that compares location using a lambda operator
    return list(filter(lambda x: x['location'] == city, data))


def get_date_object(string_date):
    """Returns a date object from a string.

    Args:
        string_date (str): Date in plain string.

    Returns:
        datetime: Object with useful methods for working with date.
    """
    return dt.datetime.strptime(string_date, '%Y-%m-%d')


def get_average_from_list(list):
    """Calculates the average from a list.

    Args:
        list (list): List of numbers.

    Returns:
        int: Average of a list.
    """
    # calculate the average by dividing the sum of numbers by the quantity of numbers
    return sum(list) / len(list)


def ask_user(path):
    """Prints out a menu and asks for users input accordingly.

    Args:
        path (str): Path to the text file that defines the menu.

    Returns:
        String if input is text, Int if input is a number.
    """
    file = open(path, encoding='utf8')
    txt = file.read()
    print(txt)
    res = input()
    if res.isdigit():
        return int(res)
    else:
        return res.lower()


def get_average_speed_per_months(city, data):
    """Calculates average speed per each month in a specified city.

    Args:
        city (str): City name.
        data (list of dict): Data to be used.

    Returns:
        dict: {
            'x': list: Months,
            'y': list: Average speeds.
            }
    """
    city = filter_by_city(city, data)
    months_dict = {}
    for dict in city:
        temp_list = []
        month = get_date_object(dict['date']).month
        if month in months_dict:
            months_dict[month].append(float(dict['download']))
        else:
            temp_list.append(float(dict['download']))
            months_dict[month] = temp_list

    avg_dict = {}
    for k, v in months_dict.items():
        avg_dict[int(k)] = get_average_from_list(v)

    items = avg_dict.items()
    pp(items)
    tuples = sorted(items)
    pp(tuples)
    # asterisk takes the tuples out of the list and spreads them out (positional expansion)
    # e.g. [1,2,3,4] > 1, 2, 3, 4
    # zip pairs items from lists together
    # e.g. [1, 2, 3], ["a", "b", "c"] > [[1, "a"], [2, "b"], [3, "c"]]
    x, y = zip(*tuples)

    return {'x': x, 'y': y}


def get_speeds_per_month(selected_month, data):
    """Returns all the speeds for a selected month.

    Args:
        selected_month (str): Full month name.
        data (list of dict): Data to be used.

    Returns:
        list: List of all speeds.
    """
    speeds = []

    # parses a month name into a month number
    month_number = str(dt.datetime.strptime(selected_month, '%B').month)
    for dict in data:
        # formats a date string into a month number
        temp_month = get_date_object(dict['date']).strftime("%m").lstrip('0')
        if month_number == temp_month:
            speeds.append(float(dict['download']))

    return speeds


def get_plot_config(label_x="x", label_y="y", ticks=10):
    """Sets desired plot config.

    Args:
        label_x (str): Name of an x label.
        label_y (str): Name of a y label.
        ticks (int): Number of ticks.
    """
    plt.tight_layout()
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.xticks(ticks)
    plt.legend(loc='best')
    plt.show()


def get_plot_theme():
    """Returns a correct plot style accrording to the state of dark mode.

    Returns:
        str: Plot style.
    """
    global dark_mode
    if dark_mode:
        return 'dark_background'
    else:
        return 'ggplot'


def parse_data():
    """Uses Parser class to parse data into a global variable."""
    global data
    data = parser.get_data(separator=',')
    input("Click ENTER to continue...")


def toggle_dark_mode():
    """Toggles a dark mode state."""
    global dark_mode
    dark_mode ^= True
    print("Dark mode is:", end=" ")
    if dark_mode:
        print(colored("ON", "green"))
        print("Open a graph to see the results.")
    else:
        print(colored("OFF", "red"))
    input("Click ENTER to continue...")


"""Makes colored terminal output work on Windows"""
colorama.init()

parser = Parser('utf8')
"""Parser: Instance of the Parser class."""

data = []
"""List: Used as a container for the parsed data."""

choice = ask_user('menu.txt')
"""String: Getting and storing users input."""

dark_mode = False
"""Boolean: Keeps track if DarkMode is ON or OFF"""


@check_data
def function2(data):
    first_month = 'August'
    second_month = 'September'
    city = 'Fanø'
    t = process_time()
    city_data = filter_by_city(city, data)
    august_speeds = get_speeds_per_month(first_month, city_data)
    september_speeds = get_speeds_per_month(second_month, city_data)
    time_elapsed = round(process_time() - t, 5)
    print(time_elapsed)
    print(f'Average download speed for {first_month} and {second_month} in {city} is:')
    print(colored(get_average_from_list(august_speeds + september_speeds), 'green'))
    input("Click ENTER to continue...")


@check_data
def function3(data):
    average_speed_ballerup = get_average_speed_per_months('Ballerup', data)
    average_speed_copenhagen = get_average_speed_per_months('Copenhagen', data)
    with plt.style.context(get_plot_theme()):
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
        get_plot_config(
            label_x="Month",
            label_y="Avg. Download speed",
            ticks=range(len(list(average_speed_ballerup['x']))+1)
        )


@check_data
def function4(data):
    city = 'Lolland'
    average_speed = get_average_speed_per_months(city, data)
    with plt.style.context(get_plot_theme()):
        plt.bar(
            average_speed['x'],
            average_speed['y'],
            label=city
        )
        get_plot_config(
            label_x="Month",
            label_y="Avg. Download speed",
            ticks=range(len(list(average_speed['x']))+1)
        )


# selecting a function based on a users choice
while choice != 'q':
    if choice == 1:
        parse_data()
    elif choice == 2:
        function2(data)
    elif choice == 3:
        function3(data)
    elif choice == 4:
        function4(data)
    elif choice == 5:
        toggle_dark_mode()
    choice = ask_user('menu.txt')
