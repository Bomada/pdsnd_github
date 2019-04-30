import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']

DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # welcome message
    print('\n' + '-'*60 + '\n\nHello! Let\'s explore some US bikeshare data! \n')
    
    # get user input for city and give warning for invalid input
    while True:
        city = input('Enter city, valid values are:\n {}\n'.format(', '.join(CITY_DATA))).lower()
        if city in CITY_DATA:
            break
        else:
            print('WARNING; \'{}\' is not a valid city, please try again.\n'.format(city))

    # get user input for month and give warning for invalid input
    while True:
        month = input('\nEnter month, valid values are:\n {}\n'.format(', '.join(MONTHS))).lower()
        if month in MONTHS:
            break
        else:
            print('WARNING: \'{}\' is not a valid month, please try again. \n'.format(month))

    # get user input for day of week and give warning for invalid input
    while True:
        day = input('\nEnter day, valid values are:\n {}\n'.format(', '.join(DAYS))).lower()
        if day in DAYS:
            break
        else:
            print('WARNING: \'{}\' is not a valid day, please try again. \n'.format(day))

    # present summary of user input
    print('\nYou have chosen to apply the following filters to the data:')
    print('City = {}'.format(city))
    print('Month = {}'.format(month))
    print('Weekday = {}\n'.format(day))
    
    # indicate end of user input section with line
    print('-'*60)
    
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
    df = pd.read_csv(CITY_DATA[city], index_col=[0])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower().str[:3] == day]

    return df


def calculate_stats(df, stats):
    """
    Displays statistics on the dataframe and stats received.

    Args:
        df - Pandas DataFrame containing city data filtered by month and weekday
        (tuple) stats - column name(s) in dataframe and description of all stats to be calculated
    """
    
    # set start time
    start_time = time.time()

    # display total trips
    total_trips = df['Start Time'].count()
    print('TOTAL NUMBER OF TRIPS: {}'.format(total_trips))
    
    # display details for input stats
    for stat in stats:
        if stat[0][0] == 'month' and len(stat[0]) == 1:
            stat_id = calendar.month_name[df.groupby(stat[0])['Start Time'].count().idxmax()]
        else:
            stat_id = df.groupby(stat[0])['Start Time'].count().idxmax()
        if type(stat_id) is tuple:
            stat_id = ', '.join(stat_id) 
        stat_freq = df.groupby(stat[0])['Start Time'].count().max()
        stat_pct = stat_freq / total_trips
        stat_desc = stat[1]
        print('{}: {} ({} trips, {:.1%})'.format(stat_desc, stat_id, stat_freq, stat_pct))
    
    # display calculation time
    print('\nThis took %s seconds.\n' % round((time.time() - start_time), 3))
    print('-'*60)
    time.sleep(1)
    

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel. Uses generic function 
    "calculate_stats" to calculate and display statistics.

    Args:
        df - Pandas DataFrame containing city data filtered by month and weekday
    """ 
    
    # define stats to calculate
    stats = ( (['month'], 'MOST FREQUENT MONTH'),
              (['day_of_week'], 'MOST FREQUENT WEEKDAY'),
              (['hour'], 'MOST FREQUENT HOUR') )
    
    # calculate and display stats defined
    print('\nCalculating The Most Frequent Times of Travel...\n')
    calculate_stats(df, stats)
        
    
def station_stats(df):
    """
    Displays statistics on the most popular stations and trip. Uses generic function 
    "calculate_stats" to calculate and display statistics.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and weekday
    """

    # define stats to calculate
    stats = ( (['Start Station'], 'MOST POPULAR START STATION'),
              (['End Station'], 'MOST POPULAR END STATION'),
              (['Start Station', 'End Station'], 'MOST POPULAR TRIP') )
    
    # calculate and display stats defined
    print('\nCalculating The Most Popular Stations and Trip...\n')
    calculate_stats(df, stats)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and weekday
    """

    # display stats to be calculated
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    total_time = df['Trip Duration'].sum()
    total_time_day = int(total_time // (24 * 3600))
    total_time_hour = round((total_time % (24 * 3600)) / 3600, 1)
    print('TOTAL TRAVEL TIME: {} days {} hours'.format(total_time_day, total_time_hour))

    # mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time_min = int(mean_time // 60)
    mean_time_sec = int(mean_time % 60)
    print('MEAN TRAVEL TIME: {} minutes {} seconds'.format(mean_time_min, mean_time_sec))
    
    # display calculation time
    print('\nThis took %s seconds.\n' % round((time.time() - start_time), 3))
    print('-'*60)
    time.sleep(1)
    

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and weekday
    """

    # display stats to be calculated
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # display counts of user types
    total_user = df['User Type'].count()
    user_value = df.groupby(['User Type']).size().rename('Count').reset_index()
    user_value = user_value.sort_values(by='Count', ascending=False)
    user_value['Pct of Total'] = round(100 * (user_value.Count / total_user), 1)
    user_value.set_index('User Type', inplace=True)
    print('USER TYPE DISTRIBUTION:\n{}\n'.format(user_value))
    
    # display counts of gender
    if 'Gender' in df.columns:
        df[['Gender']] = df[['Gender']].fillna(value='Unknown')
        total_gender = df['Gender'].count()
        gender_value = df.groupby(['Gender']).size().rename('Count').reset_index()
        gender_value = gender_value.sort_values(by='Count', ascending=False)
        gender_value['Pct of Total'] = round(100 * (gender_value.Count / total_gender), 1)
        gender_value.set_index('Gender', inplace=True)
        print('GENDER DISTRIBUTION:\n{}\n'.format(gender_value))
    else:
        print('GENDER DISTRIBUTION:\nNo gender data is available for city chosen.\n')

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_1 = df['Birth Year'].agg([min, max])
        birth_year_1.rename(index={'min':'Earliest', 'max':'Most Recent'}, inplace=True)
        birth_year_common = df.groupby(['Birth Year'])['Birth Year'].count().idxmax()
        birth_year_2 = pd.Series([birth_year_common], index=['Most Common'], name='Birth Year')
        birth_year = pd.DataFrame(pd.concat([birth_year_1, birth_year_2], axis=0))
        birth_year['Birth Year'] = birth_year['Birth Year'].astype(int)
        print('BIRTH YEAR DETAILS:\n{}'.format(birth_year))
    else:
        print('BIRTH YEAR DETAILS:\nNo birth year data is available for city chosen.\n')
        
    # display calculation time
    print('\nThis took %s seconds.\n' % round((time.time() - start_time), 3))
    print('-'*60)
    time.sleep(1)

    
def present_data(df):
    """
    Present raw data for the specified city and filters by month and day if applicable.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # information about which part of program is run
    print('\nDisplaying raw data details...')
    
    # set counter to be used when presenting row data
    row_start = 0
    
    # ask user if they want to see raw data
    while True:
        # prompt for user input
        if row_start == 0:
            restart = input('\nWould you like to see raw data for 5 trips? Enter yes or no.\n')
        else:
            restart = input('\nWould you like to see 5 more trips? Enter yes or no.\n')
        
        # restart or stop function
        if restart.lower() != 'yes':
            print('\n' + '-'*60)
            break
        
        # present raw data
        for i in range(row_start, row_start + 5):
            if i <= len(df):
                df_transposed = df.iloc[i]
                print('\nTRIP {}:\n--------\n{}'.format(i+1, df_transposed.T.to_string()))
        
        # increase row start with 5
        row_start += 5
    

def main():
    try:
        while True:
            # get user input
            city, month, day = get_filters()
            
            # load data
            df = load_data(city, month, day)

            # calculate statistics
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            # present raw data
            present_data(df)

            # restart or stop program
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                print('\n' + '-'*60)
                break
    except KeyboardInterrupt:
        print('\n' + '-'*60 + '\n\nWARNING; program interrupted by user.')
    except:        
        print('\n' + '-'*60 + '\n\nWARNING; unknown exception, program will close.')
    finally:
        print('\nProgram has been ended.\n\n' + '-'*60)


if __name__ == "__main__":
	main()
