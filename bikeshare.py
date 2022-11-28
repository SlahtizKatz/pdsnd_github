import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
months = ('january', 'february', 'march', 'april', 'may', 'june')
weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

    """ Final Review
        Ask function to ask for input"""

def ask(question, option=('y', 'n')):
    while True:
        ask = input(question).lower().strip()
        if ',' in ask:
            ask = [i.strip().lower() for i in ask.split(',')]
            if list(filter(lambda x: x in option, ask)) == ask:
                break
        elif ',' not in ask:
            if ask in option:
                break
            elif 'all' in ask:
                ask = [y.strip().lower() for y in option]
                break

        question = ("Please enter new input. \n")
        
    return ask

def get_filters():
    
    """ Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter """
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ask("What city(chicago, new york city, washington)?", CITY_DATA.keys())
    month = ask("Which month from January to June?", months)
    day = ask("Which weekday?", weekdays)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """ Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day """
    
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])
        
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print('-'*40)
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print(str(months[most_common_month-1]).title())

    # Display the most common day of week
    most_common_day = str(df['Weekday'].mode()[0])
    print(most_common_day)

    # Display the most common start hour
    most_common_hour = str(df['Start Hour'].mode()[0])
    print(most_common_hour + "h")

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # Display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("Common Start: " + most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("Common End: " + most_common_end_station)

    # Display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' -> ' + df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print(most_common_start_end_combination)
    
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = ("Total Time: " + str(int(total_travel_time//86400)) + 'd ' + str(int((total_travel_time % 86400)//3600)) + 'h ' + str(int(((total_travel_time % 86400) % 3600)//60)) + 'm ' + str(int(((total_travel_time % 86400) % 3600) % 60)) + 's')
    print(total_travel_time)
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Time: " + str(int(mean_travel_time//60)) + 'm ' + str(int(mean_travel_time % 60)) + 's')
    
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print(user_types)

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print(gender_distribution)
    except KeyError:
        print("No Data")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("Youngest Birth Year: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("Most Recent Birth Year: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("Most Common Birth Year: " + most_common_birth_year)
    except:
        print("No Data")

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        while True:
            input = ask("Type the information you want among: \n\n Time Stats [ts] \n\n Station Stats [st] \n\n Trip Duration Stat [ds] \n\n User Stat [us] \n\n Back \n\n", ('ts', 'st', 'ds', 'us', 'back'))
            if input == 'ts':
                time_stats(df)
            if input == 'st':
                station_stats(df)
            if input == 'ds':
                trip_duration_stats(df)
            if input == 'us':
                user_stats(df)
            elif input == 'back':
                break
                
        restart = ask("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()