# import necessary libraries
import pandas as pd
import os
import time
import datetime as dt

PATH = "/Users/akinbodebams/Documents/projects/BIKESHARE/bikeshare_data_analysis"
files = os.listdir(PATH)
CITY_LIST = list(filter(lambda f: f.endswith('.csv'), files))
MONTH_LIST = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'none']

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
    # invalidinputs
    city = ''
    while city not in USER_CITY_INPUT:
        city = input('Which city from the given list would you like to get information on ? Type "Ch" for Chicago , \
"Ny" for New York and "Wa" for Washington.\n').lower()
        if city not in USER_CITY_INPUT:
            city = input(f'you entered {city}, Please Type "Ch" for Chicago ,"Ny" for New York and "Wa" for '
                         'Washington.\n').lower()
        else:
            break

    # get user to enter month name
    month = ''
    while month not in MONTH_LIST:
        month = input('Do you want to filter by month? If yes, then type first three letter of month of choice , if\
not type None\n').lower()
        if month not in MONTH_LIST:
            print('Please enter a valid month name')
        else:
            break

    # get user enter week name
    day_dict = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday',
                'sat': 'Saturday', 'sun': 'Sunday', 'no': 'no'}
    day = ''
    while day not in day_dict:
        day = input('Do you want to filter by day? If yes, then type out the first three letters of day of choice e.g \
        mon, tue,wed If not, type in no\n').lower()
        if day not in day_dict:
            print('Please enter a valid day')
        else:
            break

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
    df = pd.read_csv(CITY_DICT[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new columns for month and day
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    return df
def month_data(month):
    month_dict = {'jan': 1 , 'feb': 2 , 'mar':}
    month = ''
    while month not in MONTH_LIST:
        month = input('Do you want to filter by month? If yes, then type first three letter of month of choice , if\
    not type None\n').lower()
        if month not in MONTH_LIST:
            print('Please enter a valid month name')
        else:
            break
    return month

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = df['month'].mode()[0]
    print(f'The most popular month is {popular_month}')

    # display the most common day of week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    popular_day = df['day_of_week'].mode()[0]
    # popular_day = days_of_week[num]
    print(f'The most popular day of week for start time is {popular_day}.')

    # display the most common start hourc
    pop_hour = df['Start Time'].dt.hour.mode()[0]

    def timer(pp):
        if pop_hour > 12 and pop_hour < 24:
            pp = str(pop_hour - 24) + 'pm'
        elif pop_hour < 12 and pop_hour > 0:
            pp = str(pop_hour) + 'am'
        return pp

    print(f'The most popular hour of week for start time is {pop_hour} or {timer(pop_hour)}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_startstation = df.mode()['Start Station'][0]
    print(f'The most used Start Station is {most_common_startstation}')

    # TO DO: display most commonly used end station
    most_common_endstation = df.mode()['End Station'][0]
    print(f'The most used End Station is {most_common_endstation}')

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df['Start Station'] + ' and ' + df['End Station']
    print(f'The most popular combination is: {most_common_combination.mode()[0]}')

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
    values = df['User Type'].value_counts()
    user_type = df['User Type'].unique()
    print(f'There are {len(user_type)} kinds of users  ,which are {user_type} with values of \n{values}')
    print('\n')
    # TO DO: Display counts of gender
    try:
        g_values = df['Gender'].value_counts()
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


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
