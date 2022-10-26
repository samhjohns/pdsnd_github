import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("\nWhich city would you like to filter by? Type in (new york city, chicago, washington)\n")
        city = city.lower()
        if city == "washington":
            print("\nNote: Washington data does not include gender or date of birth\n")
        if city not in ("new york city", "chicago", "washington"):
            print("Please type one of the three cities provided above.")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month = input("\nWhich month would you like to filter by? Type in (january, february, march, april, may, june, or all)\n")
        month = month.lower()
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("Please type one of the responses provided above.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("\nWhich day of the week would you like to filter by? Type in (sunday, monday, tuesday, wednesday, thursday, friday, saturday, all)\n")
        day = day.lower()
        if day not in ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"):
            print("Please type one of the responses provided above.")
            continue
        else:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and weekday from the Start Time column to create 2 new  columns
    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.weekday_name

    #filter by month
    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        #create new DataFrame filtered by month
        df = df[df["month"] == month]

    #filter by weekday
    if day != "all":

        #create new DataFrame filtered by weekday
        df = df[df["day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df["month"].mode()[0]
    print("The most common month: ", popular_month)

    # TO DO: display the most common day of week
    popular_day = df["day"].mode()[0]
    print("The most common weekday: ", popular_day)

    # TO DO: Extract hour from the Start Time column in order to display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]
    print("The most common hour of the day: ",popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used Start Station: ", df["Start Station"].value_counts().idxmax(), "\n")

    # TO DO: display most commonly used end station
    print("The most commonly used End Station: ", df["End Station"].value_counts().idxmax(), "\n")

    # TO DO: display most frequent combination of start station and end station trip
    df["Combination"] = df["Start Station"] + " to " + df["End Station"]
    print("The most frequent combination of start and end station trip: ", df["Combination"].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = sum(df["Trip Duration"])
    print("The total travel time (in days): ", total_travel_time/(24*60*60))

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("The mean travel time (in minutes): ", mean_travel_time/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df["User Type"].value_counts()
    print("User Types:\n", user_types)

    # TO DO: Display counts of gender
    if city == "washington":
        print("\nSadly Washington did not include data on customers gender or date of birth.")
    else:
        gender = df["Gender"].value_counts()
        print(gender)

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_yob = df["Birth Year"].min()
        most_recent_yob = df["Birth Year"].max()
        most_common_yob = df["Birth Year"].mode()[0]
        print("The earliest birth year: ", earliest_yob, "\n")
        print("The most recent birth year: ", most_recent_yob, "\n")
        print("The most common birth year: ", most_common_yob, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    pd.set_option("display.max_columns", 200)
    x=1
    while True:
        raw_data = input("\nWould you like to see some raw data? (y or n)\n")
        if raw_data.lower() == "y":
            print(df[x:x+5])
            x = x+5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
