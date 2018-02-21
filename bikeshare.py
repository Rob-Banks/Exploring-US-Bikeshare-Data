#imports
import csv
import pandas
import time
import datetime
import calendar

################################################################################

# Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


weekdays = list(calendar.day_name)
months = list(calendar.month_name)
num_days = []
for i in range(1, 7):
    num_days.append(calendar.monthrange(2017,i)[1])

################################################################################

def get_city():
    '''
    Asks the user for a city and returns the filename for that city's bike
    share data.

    Args:
        none.
    Returns:
        (str) Selected city's filename of bikeshare data.
    '''

    city = input('\nWould you like to see data for Chicago, New York,'
                    ' or Washington? (You may quit by typing "quit")\n')
    if city.lower() == 'chicago':
        return city, chicago
    elif city.lower() == 'new york':
        return city, new_york_city
    elif city.lower() == 'washington':
        return city, washington
    elif city.lower() == 'quit':
        return None
    else:
        print("Please enter Chicago, New York, or Washington")
        return get_city()

################################################################################

def get_time_period():
    '''
    Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) specified time filter, (int) month in a 12 calendar year, (int) day in month
    '''

    time_period = input('\nWould you like to filter the data by month, day, or'
                        ' not at all? Type "none" for no time filter.\n')
    month = None
    day = None

    if time_period.lower() == 'month':
        month = get_month()
        return time_period, month, day
    elif time_period.lower() == 'day':
        month = get_month()
        day = get_day(month)
        return time_period, month, day
    elif time_period.lower() == 'none':
        return time_period, month, day
    else:
        print("Incorrect filter type")

################################################################################

def get_month():
    '''
    Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (str) Month user requested from 1 to 6
    '''

    month = input('\nWhich month? January, February, March, April, May,'
                    ' or June?\n')
    if month.title() in months[:7]:
        return str(months.index(month.title())).zfill(2)
    else:
        print("Incorrect input. Must be from January to June")

################################################################################

def get_day(month):
    '''
    Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int) Day in month (1 - 31)
    '''

    day = int(input('\nWhich day? Please type your response as an integer from 1 - 31.\n'))

    if 1 <= day <= num_days[int(month) - 1]:
        return str(day).zfill(2)
    elif day >= 32:
        print('Incorrect input. Enter real positive number not to exceeding 31')
        return get_day(month)
    else:
        print("Incorrect input. Enter number from 1 - 31")

################################################################################

def popular_month(city_file):
    '''
    Counts occurences of months and outputs popular month

    Args:
        (str) filename
    Returns:
        (str) Name of month with the most rides purchased

    Question: What is the most popular month for start time?
    '''

    city_file['Month - Start Time'] = city_file['Start Time'].str[5:7]

    popular_month_int = int(city_file['Month - Start Time'].mode().iloc[0])
    popular_month_str = datetime.date(2017, popular_month_int, 1).strftime('%B')
    return popular_month_str

################################################################################

def popular_day(city_file):
    '''
    Takes .csv file for city and outputs most popular day

    Args:
        (str) Filename
    Returns:
        (str) Day of the week with the most rides purchased


    Question: What is the most popular day of week (Monday, Tuesday, etc.) for
    start time?
    '''

    city_file['Day of Week'] = pandas.to_datetime(city_file['Start Time']).apply(
                            lambda x: x.weekday())
    popular_day_int = city_file['Day of Week'].mode().iloc[0]
    popular_day_str = weekdays[popular_day_int]
    return popular_day_str

################################################################################

def popular_hour(city_file):
    '''
    Calulates the hour with the most purchases

    Args:
        (str) filename
    Returns:
        (str) Popular hour of the Day

    Question: What is the most popular hour for start time?
    '''

    city_file['Hour - Start Time'] = city_file['Start Time'].str[-8:-6]
    popular_hour_str = str(city_file['Hour - Start Time'].mode().iloc[0])
    return popular_hour_str

################################################################################

def trip_duration(city_file):
    '''
    Calulates the total duration and average duration of all purchases

    Args:
        (str) filename
    Returns:
        (str) Total duration of trips (float) Average Duration

    Question: What is the total trip duration and average trip duration?
    '''

    total_time = city_file['Trip Duration'].sum()
    average_time = city_file['Trip Duration'].mean()
    return total_time, average_time

################################################################################

def popular_stations(city_file):
    '''
    Determines the popular starting and ending points

    Args:
        (str) filename
    Returns:
        (str) Start Station (str) End Station
    Question: What is the most popular start station and most popular end
    station?
    '''

    ss = city_file['Start Station'].mode().iloc[0]
    es = city_file['End Station'].mode().iloc[0]
    return ss, es

################################################################################

def popular_trip(city_file):
    '''
    Determines the most common trip

    Args:
        (str) filename
    Returns:
        (str) Popular Trip
    Question: What is the most popular trip?
    '''

    city_file['Trip'] = 'FROM: ' + city_file['Start Station'] + '\nTO:   ' + city_file['End Station']
    trip = city_file['Trip'].mode().iloc[0]
    return trip

################################################################################

def users(city_file):
    '''
    Determines how many customers and subscribers

    Args:
        (str) filename
    Returns:
        (int) Customers (int) Subscribers
    Question: What are the counts of each user type?
    '''

    cust = city_file['User Type'].value_counts()['Customer']
    subs = city_file['User Type'].value_counts()['Subscriber']
    return cust, subs

################################################################################

def gender(city_file):
    '''
    Determines how many Males and Females

    Args:
        (str) filename
    Returns:
        (int) Males (int) Females
    Question: What are the counts of gender?
    '''
    if 'Gender' in city_file:
        male = city_file['Gender'].value_counts()['Male']
        female = city_file['Gender'].value_counts()['Female']
    else:
        return 0, 0
    return male, female

################################################################################

def birth_years(city_file):
    '''
    Determines how youngest, oldest and common birthyears

    Args:
        (str) filename
    Returns:
        (int) Oldest user (int) Youngest user (int) Average user
    Question: What are the earliest, most recent, and most popular birth years?
    '''

    if 'Birth Year' in city_file:
        oldest = int(city_file['Birth Year'].min())
        youngest = int(city_file['Birth Year'].max())
        mode = int(city_file['Birth Year'].mode().iloc[0])
    else:
        return 'NaN', 'NaN', 'Nan'
    return oldest, youngest, mode

################################################################################

def display_data(city_file):
    '''
    Displays five lines of data if the user specifies that they would
    like to and continues to ask the user whether to see five more until 'no'
    args:
        (str) filename for a city's bikeshare data
    Returns:
        none
    '''
    display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. ')

    i = 5
    j = 0

    while display == 'yes':
        print(city_file[j:i])
        print('\n')
        i += 5
        j += 5
        display = input('Would you like to view individual trip data?'
                        'Type \'yes\' or \'no\'. ')

################################################################################

def filter_boi(city_file, month, day):
    '''
    Filters file for users selected time frame
    args:
        (str) filename
    Returns:
        (pandas dataframe) Remaining file
    '''

    city_file = pandas.read_csv(city_file)
    if month != None:
        city_file['Month'] = pandas.to_datetime(city_file['Start Time']).apply(
                        lambda x: x.strftime("%B"))
        city_file = city_file[city_file['Month'] == months[int(month)]]
    if day != None:
        city_file['Day'] = pandas.to_datetime(city_file['Start Time']).apply(
                        lambda x: x.strftime("%d"))
        city_file = city_file[city_file['Day'] == day]
    return city_file

################################################################################

def statistics():
    '''calculates and prints out the descriptive statistics about a city
    and time period specified by the user via raw input
    args:
        none
    Returns:
        none
    '''

    print("\nWelcome to Bikeshare Analysis!\n\nThis program will use data obtained from Motivate and guide you to obtain some relevent statistics on bike sharing user base.")
    print("\nLet's get started!\n")

    # Filter by city (Chicago, New York, Washington)
    city, city_file = get_city()

    # Filter by time period (month, day, none)
    time_period, month, day = get_time_period()

    # Filters file to reduce processing time
    city_file = filter_boi(city_file, month, day)

    if month != None:
        month_str = datetime.date(2017, int(month), 1).strftime('%B')
    else:
        month_str = 'all months'

    print('\nCalculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()

        # Calls popular_month function and print the results
        print("\nThe most popular month in {} 2017 is: ".format(city))
        print(popular_month(city_file))

        print("\nThat took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday...) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        # Calls popular_day function and print the results
        print("\nThe most popular day in {} is: ".format(city))
        print(popular_day(city_file))

        print("\nThat took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")


    start_time = time.time()

    # What is the most popular hour of day for start time?
    # Calls popular_hour function and print the results
    print("\nThe most popular hour in {} is: ".format(city))
    print(popular_hour(city_file))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    # Calls trip_duration function and print the results
    tot, ave = trip_duration(city_file)
    tot = int(tot)
    hours = tot // 3600
    minutes = (tot % 3600) // 60
    seconds = tot % 60
    print("\nThe total time rode in {} is: ".format(city))
    print("{} hours {} minutes {} seconds".format(hours, minutes, seconds))
    print("\nThe average time rode in {} is: ".format(city))
    print('%.2f seconds' % ave)

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    # Calls popular_stations function and print the results
    start_station, end_station = popular_stations(city_file)
    print("\nThe most popular start station in {} is: ".format(city))
    print(start_station)
    print("\nThe most popular end station in {} is: ".format(city))
    print(end_station)

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    # Calls popular_trip function and print the results
    print("\nThe most popular trip in {} is: ".format(city))
    print(popular_trip(city_file))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type? 'Customer' or 'Subscriber'
    # Calls users function and print the results
    customers, subscribers = users(city_file)
    print("\nTotal customers: ")
    print(customers)
    print("\nTotal subscribers: ")
    print(subscribers)

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    # Calls gender function and print the results
    if city.lower() == 'washington':
        print("\nThere is no Gender data for Washington")
    else:
        males, females = gender(city_file)
        print("Total males:")
        print(males)
        print("Total females :")
        print(females)

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the earliest, most recent, and most popular birth years?
    # Calls birth_years function and print the results
    if city.lower() == 'washington':
        print("There is no birth year data for Washington")
    else:
        oldest, youngest, mode = birth_years(city_file)
        print("The earliest birth year is: ")
        print(oldest)
        print("The most recent birthyear is: ")
        print(youngest)
        print("The popular birthyear is: ")
        print(mode)

    print("That took %s seconds.\n" % (time.time() - start_time))

    # Displays five lines of data at a time if user specifies that they would like to
    display_data(city_file)

    # Restart?
    restart = input("\nWould you like to restart? Type 'yes' or 'no'.\n")
    if restart.lower() == 'yes':
        statistics()

################################################################################

if __name__ == "__main__":
	statistics()
