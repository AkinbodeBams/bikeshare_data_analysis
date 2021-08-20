# import necessary libraries
import os
import time
import pandas as pd

#linking part code to path
CITY_LIST = ['chicago.csv', 'new_york_city.csv', 'washington.csv']
MONTH_LIST = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'none']
DAY_LIST = ['mon', 'tue', 'wed', 'thu', 'fri','sat','sun', 'none']
USER_CITY_INPUT = ['ch', 'ny', 'wa']
CITY_DICT = {USER_CITY_INPUT[i]: CITY_LIST[i] for i in range(len(CITY_LIST))}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello User, welcome to Bikeshare!! \nWe have the first six month Data on the following cities : Chicago, \
New York and Washington.')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle
    # invalid inputs

    city = ''
    # looping until expected input is given
    while city not in USER_CITY_INPUT:
        city = input('Which city from the given list would you like to get information on ? Type "Ch" for Chicago , \
"Ny" for New York and "Wa" for Washington.\n').lower()
        if city not in USER_CITY_INPUT:
            city = input(f'you entered "{city}", Please Type "Ch" for Chicago ,"Ny" for New York and "Wa" for '
                         'Washington.\n').lower()
        else:
            break
    city = CITY_DICT[city]
    #linking user shortened response to standard or daframes recognizable value
    month_dict = {'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April', 'may': 'May', 'jun': 'June',
                  'none': 'none'}
    # get user to enter month name
    month = ''
    # loops until expected response is met
    while month not in MONTH_LIST:
        month = input('Do you want to filter by month? If yes, type the first three letters of month of your choice e.g jan\
, if not type None\n').lower()
        if month not in MONTH_LIST:
            month = input(f'You entered {month}, Please enter a valid month name e.g: jan ...jun\n')
        else:
            break
    #returns the  appropriate month
    month = month_dict[month]

    # get user enter week name
    day_dict = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday',
                'sat': 'Saturday', 'sun': 'Sunday', 'none': 'none'}
    day = ''
    while day not in DAY_LIST:
        day = input('Do you want to filter by day? If yes, then type out the first three letters of day of choice e.g \
mon, tue,wed If not, type in none \n').lower()
        if day not in DAY_LIST:
            day = input(f'You entered {day}, Please enter a valid day e.g mon')
        else:
            break
    day = day_dict[day]

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load provided city
    df = pd.read_csv(city)

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new columns for month and day
    df['hour'] = df['Start Time'].dt.hour
    df['month_name'] = df['Start Time'].dt.month_name()
    df['day_name'] = df['Start Time'].dt.day_name()

    if month != 'none':
        df['month_filtered'] = month

    if day != 'none':
        df['day_filtered'] = day

    # filter by month
    if month == 'none':
        pass
    else:
        df = df[df['month_name'] == month]

    if day == 'none':
        pass
    else:
        df = df[df['day_name'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
        display most occurring month if user  chooses not to filter by month
        display most occurring day if user chooses not to filter by day
        display both month and day if users chooses not use any filtering"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    def time_filter(data):
        """filters response based on user's filter choice"""

        if 'month_filtered' in df.columns and 'day_filtered' in data.columns:
            pass
        elif 'month_filtered' in df.columns and 'day_filtered' not in data.columns:
            print(f"{data['day_name'].mode()[0]} is the most occurring day in the month provided .")
        elif 'month_filtered' not in df.columns and 'day_filtered' in data.columns:
            print(f"{data['month_name'].mode()[0]} is the most occurring month in the data .")
        else:
            print(f"{data['month_name'].mode()[0]} is the most occurring month in the data without any filtering .")

    # TO DO: display the most common month
    time_filter(df)

    # TO DO: display the most common start hour
    pop_hour = int(df['hour'].mode()[0])

    def timer(pp):
        """ converts time from 24hrs to am and or pm """
        if 12 < pop_hour < 24:
            pp = str(abs(pop_hour - 12)) + 'pm'
        elif 12 > pop_hour > 0:
            pp = str(abs(pop_hour)) + 'am'
        return pp

    if 'month_filtered' in df.columns and 'day_filtered' in df.columns:
        print(f'The most popular hour for start time in chosen Month and Day is {pop_hour}:00hrs or {timer(pop_hour)}.')
    elif 'month_filtered' in df.columns and 'day_filtered' not in df.columns:
        print(f'The most popular hour for start time in chosen Month is {pop_hour}:00hrs or {timer(pop_hour)}.')
    elif 'month_filtered' not in df.columns and 'day_filtered' in df.columns:
        print(f'The most popular hour for start time in chosen Day is {pop_hour}:00hrs or {timer(pop_hour)}.')
    else:
        print(f'The most popular hour for start time in general is {pop_hour}:00hrs or {timer(pop_hour)}.')

    # Analysing Gender Distribution if Gender column exist in provided data
    try:
        gender = df["Gender"].mode()[0]
        if 'month_filtered' in df.columns and 'day_filtered' in df.columns:
            print(f'The {gender} gender made more use of this services for the Provided Month and Day')
        elif 'month_filtered' in df.columns and 'day_filtered' not in df.columns:
            print(f'The {gender} gender made more use of this services for the Provided Month')
        elif 'month_filtered' not in df.columns and 'day_filtered' in df.columns:
            print(f'The {gender} gender made more use of this services for the given Day')
        else:
            print(f'The {gender} gender made more use of this services in general ')
    except KeyError as e:
        print(f'sorry we don\'t have data {e} for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start_station = 'Start Station'
    end_station = 'End Station'

    def station(stations):
        """displays statistics based on provided station and user's filter choice"""

        station_mode = df.mode()[stations][0]
        if 'month_filtered' in df.columns and 'day_filtered' in df.columns:
            print(f'The most used {stations} based on provided month and day is {station_mode}')
        elif 'month_filtered' in df.columns and 'day_filtered' not in df.columns:
            print(f'The most used {stations} based on provided month is {station_mode}')
        elif 'month_filtered' not in df.columns and 'day_filtered' in df.columns:
            print(f'The most used {stations} based on provided day is {station_mode}')
        else:
            print(f'The most used {stations} based on provided day is {station_mode}')

    def combined_station(start_s, end_s):
        """displays statistics based on provided station and user's filter choice"""

        combination = 'From ' + start_s + ' to ' + end_s
        if 'month_filtered' in df.columns and 'day_filtered' in df.columns:
            print(f'The most popular combination for month and day  chosen is: {combination.mode()[0]}')
        elif 'month_filtered' in df.columns and 'day_filtered' not in df.columns:
            print(f'The most popular combination is: {combination.mode()[0]}')
        elif 'month_filtered' not in df.columns and 'day_filtered' in df.columns:
            print(f'The most popular combination is: {combination.mode()[0]}')
        else:
            print(f'The most popular combination is: {combination.mode()[0]}')

    # TO DO: display most commonly used start station
    station(start_station)
    # TO DO: display most commonly used end station
    station(end_station)
    # TO DO: display most frequent combination of start station and end station trip
    combined_station(df['Start Station'], df['End Station'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total = df['Trip Duration'].sum()
    day = round(total // (24 * 3600))
    total = total % (24 * 3600)
    hour = round(total // 3600)
    total %= 3600
    minutes = round(total // 60)
    total %= 60
    seconds = round(total)

    # TO DO: display total travel time
    print(f'Total time traveled is {day} days, {hour} hours, {minutes} minutes and {seconds} seconds')
    average = df['Trip Duration'].mean()
    avg_minutes = round(average // 60)
    avg_seconds = round(average % 60)

    # TO DO: display mean travel time
    print(f'The average travel time is {avg_minutes} Minutes and {avg_seconds} Seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    values = str(df['User Type'].value_counts()).split('\n')[:-1]
    values = '\n'.join(values)
    user_type = df['User Type'].unique()
    print(f'There are {len(user_type)} kinds of users  ,which are {user_type} with values of \n{values}')
    print('\n')
    # TO DO: Display counts of gender
    try:
        g_values = str(df['Gender'].value_counts()).split('\n')[:-1]
        g_values = '\n'.join(g_values)
        if 'Gender' in df:
            print(f'The Genders distributions are \n{g_values} ')
    except KeyError as e:
        print(f'Sorry! {e} data unavailable for Washington')
    print('\n')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        popular = int(df['Birth Year'].mode()[0])
        if 'Birth Year' in df:
            print(f'The Earliest birth year is: {earliest}')
            print(f'The latest birth year is: {latest}')
            print(f'The most popular birth year is: {popular}')
    except KeyError as e:
        print(f'Sorry! {e} data unavailable for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays data if user's answer is 'yes',
    and continues iterating  prompts and displaying the random 5 lines of raw data at each iteration,
    Stop the program when the user says 'no' or there is no more raw data to display."""

    start = 0
    stop = 5
    user_input = True
    user_input2 = True
    question = ''
    while user_input:
        question = input('Would you like to see some lines of the data. Type yes or no\n').lower()
        if question == 'yes':
            print(df.iloc[start:stop, 1:-2])
            while user_input2:
                re_question = input('Would you like to see more\n').lower()
                if re_question.lower() == 'yes':
                    start += 5
                    stop += 5
                    # checks if iteration has reach it max
                    if stop == df.shape[0]:
                        user_input = False
                    print(df.iloc[start:stop, 1:-2])
                elif re_question == 'no':
                    user_input = False
                    user_input2 = False
                else:
                    print(f'you entered an invalid response [{re_question}], try again ')
        elif question == 'no':
            user_input = False
        else:
            print(f'you entered an invalid response [{question}], try again ')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Have a nice day')
            break


if __name__ == "__main__":
    main()
