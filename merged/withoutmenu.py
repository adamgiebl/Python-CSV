import csv # adds the module that is needed for parsing the CSV file
from time import process_time

def parsing(): # defines the below part as a function, so it can be run anytime, easily

    with open('data.csv', 'r') as csv_file: # opens the CSV file as a readable
        csv_reader = csv.DictReader(csv_file,delimiter = ',') # uses a function from the CSV module to assign the data from the file to dictionaries with the correct headers
        for row in csv_reader:
            print(row) # uses a for loop to print out the dictionaries

parsing()

def avrg_speed(): # defines the below part as a function, so it can be run anytime, easily
    
    sum1 = 0
    sum2 = 0 # creates variables that will be used later
    date = []
    time = []
    location = []
    dwnld = []
    upld = [] # creates empty lists
    
    with open('data.csv', 'r', encoding="utf8") as csv_file: # opens the CSV file as a readable
        csv_reader = csv.reader(csv_file,delimiter = ',')
        for row in csv_reader:
            date.append(row[0])
            time.append(row[1])
            location.append(row[2])
            dwnld.append(row[3])
            upld.append(row[4]) # uses a for loop and list function to assign the date from the CSV file to the empty lists

    t = process_time()
    all_loc = [i for i, x in enumerate(location) if x == "Fanø"] # counts all the locations which are named Fano, then assigns it to a variable
    aug_date = [i for i, x in enumerate(date) if "2018-08" in x] # counts all the dates which begin with 2018-08, then assigns it to a variable
    sep_date = [i for i, x in enumerate(date) if "2018-09" in x] # counts all the dates which begin with 2018-09, then assigns it to a variable
    aug_set = (set(all_loc) & set(aug_date)) # gets the intersection between Fano and August and puts them into a set
    sep_set = (set(all_loc) & set(sep_date)) # gets the intersection between Fano and September and puts them into a set
    aug_list = list(aug_set)
    sep_list = list(sep_set) # converts the sets to lists
    len_aug = len(aug_list)
    len_sep = len(sep_list) # counts how many elemnts are in the lists

    for t1 in range(len_aug): # uses a for loop combined with the range function, it basically counts until the list's length
        sum1 = sum1 + float(dwnld[aug_list[t1]]) # converts the August list's index numbers to the download speed data and adds them together

    for t2 in range(len_sep):  # uses a for loop combined with the range function, it basically counts until the list's length
        sum2 = sum2 + float(dwnld[sep_list[t2]]) # converts the September list's index numbers to the download speed data and adds them together

    num1 = sum1 + sum2 # adds the sums of August and September
    num2 = len_aug + len_sep # adds the number of elemts together
    avrg = num1 / num2 # divides the sums by the number of elements, therefeore counts average
    print(avrg)
    time_elapsed = round(process_time() - t, 5)
    print(time_elapsed)

avrg_speed()
