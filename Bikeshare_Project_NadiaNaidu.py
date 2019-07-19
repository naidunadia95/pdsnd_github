import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).

    month_gf = 'none'
    day_gf = 'none'

    while True:
        city_gf = input("Please enter Chicago, New York City or Washington: ").lower()
        if city_gf not in ('chicago', 'new york city', 'washington'):
            print("This is not an appropriate city, please try again!")
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        choice = input("Would you like to filter data by month, day, both or no filter at all? Enter 'none' for no time filter: ").lower()
        if choice not in ['month', 'day', 'both', 'none']:
            print("This is not a correct choice - please try again")
        else:
            break

    while choice == 'month' or choice == 'both':
        month_gf = input("To filter data by month, please enter a single month from either January, February, March, April, May or June: ").lower()
        if month_gf not in ['january', 'february', 'march', 'april', 'may', 'june']:
            print("This is not an appropriate month - try again!")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while choice == 'day' or choice == 'both':
        day_gf = input("P|lease enter a single day from either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday: ").lower()
        if day_gf not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("This is not an appropriate day - try again!")
        else:
            break

    # turning the values obtained into variables that can be used locslly or globally in other functions to be created.

    global city
    city = city_gf

    global month
    month = month_gf

    global day
    day = day_gf

    return city_gf, month_gf, day_gf


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(str(CITY_DATA[city]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    global df_ld

    df_ld = df

    return df


def time_stats(df_ld):
    """
    Displays statistics on the most frequent times of travel.

    Returns:
        (str) popular_month - names the most frequent month indexed against a list of monthly names
        (str) popular day - names the most frequent day
        (str) popular hour - names the most frequent popular_hour
        (int) counts - lists the tally of the most popular month, day and hour respectively
        (float) run time - time taken for the prompt to complete

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month

    if month == 'none':

        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        # convert the Start Time column from the csv to datetime

        df_ld['Start Time'] = pd.to_datetime(df_ld['Start Time'])

        # extracts month from the Start Time column to create an month column

        df_ld['month'] = df_ld['Start Time'].dt.month

        # find the most common month (from 1 to 12)

        popular_month = df_ld['month'].mode()[0]
        popular_month_count = df_ld['month'].value_counts(sort=True).max()

        print('The most popular month is: ', month_list[popular_month - 1])
        print('This month has a total count of: ', popular_month_count)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    # TO DO: display the most common day of week

    if day == 'none':

        # convert the Start Time column to datetime

        df_ld['Start Time'] = pd.to_datetime(df_ld['Start Time'])

        # extract day from the Start Time column to create a day column

        df_ld['day'] = df_ld['Start Time'].dt.weekday_name

        # find the most common day(from Monday to Sunday)

        popular_day = df_ld['day'].mode()[0]
        popular_day_count = df_ld['day'].value_counts(sort=True).max()

        print('The most popular day is: ', popular_day)
        print('This day has a total count of: ', popular_day_count)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    # display the most common start hour

    # convert the Start Time column to datetime

    df_ld['Start Time'] = pd.to_datetime(df_ld['Start Time'])

    # extract hour from the Start Time column to create an hour column

    df_ld['hour'] = df_ld['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df_ld['hour'].mode()[0]

    popular_hour_count = df_ld['hour'].value_counts(sort=True).max()

    print('The most popular hour is: ', popular_hour)
    print('This hour has a total count of: ', popular_hour_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df_ld):
    """
    Displays statistics on the most popular biking stations

    Returns:
        (str) popular start station - names the most frequent station where participants begin their trip
        (str) popular end station - names the most frequent station where participants end their trip
        (str) popular start-end station - names the most frequent start-end stations where participants begin and then end their trip
        (int) counts - lists the tally of the most start, end and start-end stations respectively.
        (float) run time - time taken for the prompt to complete

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df_ld['Start Station'].mode()[0]
    popular_start_count = df_ld['Start Station'].value_counts(sort=True).max()

    print("The most popular start staion is: ", popular_start_station)
    print("This start station has a total count of: ", popular_start_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # display most commonly used end station

    popular_end_station = df_ld['End Station'].mode()[0]
    popular_end_count = df_ld['End Station'].value_counts(sort=True).max()

    print("The most popular end staion is: ", popular_end_station)
    print("This end station has a total count of: ", popular_end_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # display most frequent combination of start station an end station trip

    df_ld['Station Start-End Combo'] = df_ld['Start Station'] + " " + "with" + " " + df_ld['End Station']

    station_combo_counts = df_ld['Station Start-End Combo'].value_counts(sort=True)

    highest_count = df_ld['Station Start-End Combo'].value_counts(sort=True).max()

    station_dict = dict(station_combo_counts)

    print("The start and end station comnbination(s) used most frequently is: \n")

    # This loop was added to account for start_end combinations where more than one station shared the highest value.

    for key, value in station_dict.items():
        if value > highest_count - 1:
            print(key,"\n")

    print("Here the total count of this combination(s) is: ", highest_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df_ld):
    """
    Displays statistics on trip durations.

    Returns:
        (str) trip sum time - yields the total duration cycled by across all participants under the preferred city-time filter
        (str) average trip time - yields the average duration cycled across all participants under the preferred city_time filter.
        (float) run time - time taken for the prompt to complete

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    df_ld['Trip Sum'] = df_ld['Trip Duration'].sum()

    t1 = df_ld['Trip Sum'].astype(str).str.zfill(6)

    df_ld['Trip Sum'] = t1.str[0:2] + ':' + t1.str[2:4] + ':' + t1.str[4:6]

    print("The total trip duration is: ", df_ld['Trip Sum'].max())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # display mean travel time

    trip_mean_working = str(df_ld['Trip Duration'].mean())

    trip_mean_working = trip_mean_working.split(".", 1)

    trip_mean_working = trip_mean_working[0]

    df_ld['Trip Average'] = trip_mean_working

    t2 = df_ld['Trip Average'].astype(str).str.zfill(6)

    df_ld['Trip Average'] = t2.str[0:2] + ':' + t2.str[2:4] + ':' + t2.str[4:6]

    trip_average = df_ld['Trip Average'].max()

    print("The average trip duration is: ", trip_average)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df_ld):
    """
    Displays statistics on the user types in terms of membership type, gender and birth year if applicable.

    Returns:
        (str) membership type - a total count of each category of memebership participants fall under.
        (str) gender type - a total count of each category of gender participants fall under. In cases. where gender was omitted - "Not Specified" was introduced
        (int) yougest birth year - names the birth year of the eldest participant using these biking services.
        (int) eldest birth year - names the birth year of the youngest participant using these biking services.
        (int) common birth year - names the most frequent birth year across participants using these biking services.
        (int) counts - lists the tally of the most start, end and start-end stations respectively.
        (float) run time - time taken for the prompt to complete

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types

    df_ld['User Type'] = df_ld['User Type'].fillna("Not Specified")

    user_types = df_ld['User Type'].value_counts()

    print("User categories and their participant numbers include: \n")
    print(user_types)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # display counts of gender
    if city != 'washington':

        df_ld['Gender'] = df_ld['Gender'].fillna("Not Specified")
        gender_types = df_ld['Gender'].value_counts()

        print("Gender categories and their participant numbers include: \n")
        print(gender_types, "\n")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print("Unfortunately no gender statistics were apparent for this city.")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    # TO DO: Display earliest, most recent, and most common year of birth

    if city != 'washington':

        oldest_year = df_ld['Birth Year'].min()

        youngest_year = df_ld['Birth Year'].max()

        popular_year = df_ld['Birth Year'].mode()[0]

        df_ld['Birth Year'] = df_ld['Birth Year'].fillna('Not Specified')

        print("The oldest year in this filter is: ", int(oldest_year))
        print("The earliest year in this filter is: ", int(youngest_year))
        print("The most popular birth year is: ", int(popular_year))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print("Unfortunately no birth year statistics were apparent for this city")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def raw_data(df_ld):
    """
    Asks user to specify whether they would like to see 5 rows of raw data.

    Returns:
        (pandas dataframe) raw data - displays raw data
    """

    # creating dictionary for cities where all columns of data are present; if not some other dictionary must be created to account for missing data.

    if city != 'washington':
        raw_dict = {'Start Time': df_ld['Start Time'], 'End Time': df_ld['End Time'], 'Trip Duration': df_ld['Trip Duration'], 'Start Station': df_ld['Start Station'], 'End Station': df_ld['End Station'], 'User Type': df_ld['User Type'], 'Gender': df_ld['Gender'], 'Birth Year': df_ld['Birth Year']}
    else:
        raw_dict = {'Start Time': df_ld['Start Time'], 'End Time': df_ld['End Time'], 'Trip Duration': df_ld['Trip Duration'], 'Start Station': df_ld['Start Station'], 'End Station': df_ld['End Station'], 'User Type': df_ld['User Type']}

    raw_dataframe = pd.DataFrame(raw_dict)

    counter = 5

    # prompts user to display data

    while True:
        see_data = input("Would you like to see five rows of raw data? Please enter 'yes' or 'no': ")
        if see_data not in ['yes', 'no']:
            print("That is an invalid option.")
        elif see_data in ['yes']:
            print(raw_dataframe.iloc[:counter])
            counter += 5
        else:
            break

    print("Thank you for using this program, goodbye!")


def main():
    get_filters()
    load_data(city, month, day)
    time_stats(df_ld)
    station_stats(df_ld)
    trip_duration_stats(df_ld)
    user_stats(df_ld)
    raw_data(df_ld)


main()
