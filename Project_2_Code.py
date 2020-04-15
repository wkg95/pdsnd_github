import pandas as pd
import numpy as np
import datetime as dt
import calendar as ca
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

print('Hello! Let\'s explore some US bikeshare data!\n')
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    If inputs are not valid, function will ask user to restart the program.

    """
    while True:
        city = input('\nWould you like to see bikeshare data for Chicago, New York, or Washington?\n').lower()
        if city != 'chicago' and city != 'new york' and city != 'washington':
            print('That is not a valid city. You will need to restart the program!')
        month = input('\nWould you like to filter the data by month? Please enter January, February, March, April, May, or June. If you do not want to filter by month, enter All\n').lower()
        if month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june' and month!= 'all':
            print('That is not a valid answer. You will need to restart the program!')
        day = input('\nWould you like to filter the data by day of the week? Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday. If you do not want to filter by day of the week, enter All\n').lower()
        if day != 'sunday' and day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'frieday' and day != 'saturday' and day != 'all':
            print('That is not a valid answer. You will need to restart the program!')
        print('-'*40)
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

    months = {'all':0, 'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
    days = {'all':0, 'monday':1, 'tuesday':2, 'wednesday':3, 'thursday':4, 'friday':5, 'saturday':6, 'sunday':7}
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df.insert(2,'Month', df['Start Time'].dt.month)
    df.insert(3,'Day', df['Start Time'].dt.weekday + 1)
    if months[month] > 0:
        df = df[df['Month'] == months[month]]
    if days[day] > 0:
        df = df[df['Day'] == days[day]]
    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['Hour'] = df['Start Time'].dt.hour
    popular_month = df['Month'].mode()[0]
    popular_month_name = ca.month_name[popular_month]
    popular_day = df['Day'].mode()[0]
    popular_day_name = ca.day_name[popular_day]
    popular_hour = df['Hour'].mode()[0]
    print('Most Frequent Start Month: ', popular_month_name)
    print('Most Frequent Start Day of Week: ', popular_day_name)
    print('Most Frequent Start Hour (24-Hour Clock): ', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    popular_trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('Most Frequent Start Station: ', popular_start_station)
    print('Most Frequent End Station: ', popular_end_station)
    print('Most Frequest Route: ', popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):

    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = (df['Trip Duration'] / 3600).sum()
    avg_travel_time= (df['Trip Duration'] / 60).mean()
    print('Total Travel Time in Hours: ', total_travel_time)
    print('Average Travel Time in Minutes: ', avg_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(city, df):

    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    count_user_type = (df['User Type']).value_counts()
    print('Number of customers and subscribers:\n', count_user_type)
    if city == 'washington':
        print('Sorry! There is no gender or year of birth data available for Washington.')
    else:
        count_gender = (df['Gender']).value_counts()
        print('Number of males and females:\n', count_gender)
        earliest_yob = int(min(df['Birth Year']))
        latest_yob = int(max(df['Birth Year']))
        popular_yob = int(df['Birth Year'].mode()[0])
        print('Earliest birth year: ', earliest_yob)
        print('Latest birth year: ', latest_yob)
        print('Most common birth year: ', popular_yob)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    """Asks user if they want to see raw data by the filters 5 rows at a time."""

    counter = 0
    five_lines = input('\nDo you want to see 5 lines of raw data? Enter Yes or No.\n')
    while True:
        if five_lines == 'Yes':
            print(df.iloc[counter : counter + 5])
            counter += 5
            five_lines = input('\nDo you want to see more raw data? Enter Yes or No.\n')
        else:
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart != 'Yes':
            break

if __name__ == "__main__":
	main()
