import time
import pandas as pd

# Define city data.
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
# Function asks user to specify a city, month, and day to analyze.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please choose from Chicago, New York City, or Washington.')
    
    # Get user input for month
    while True:
        month = input('Which month? January, February, March, April, May, June, or all?').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Invalid input. Please choose a valid month or "all" for all months.')
    
    # Get user input for day of week
    while True:
        day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?').lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Invalid input. Please choose a valid day of the week or "all" for all days.')
    
    print('-'*40)
    return city, month, day
# Function loads data for the specified city and filters by month and day if applicable. 
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df
# Function display statistics on the most frequent times of travel
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['Month'].mode()[0]
    print(f"The most common month for travel is: {common_month}")

    common_day_of_week = df['Day of Week'].mode()[0]
    print(f"The most common day of the week for travel is: {common_day_of_week}")

    df['Hour'] = df['Start Time'].dt.hour
    common_start_hour = df['Hour'].mode()[0]
    print(f"The most common start hour for travel is: {common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
# Function display statistics on the most popular stations and trip.
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    df['Combined Stations'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Combined Stations'].mode()[0]
    print(f"The most frequent combination of start and end stations is: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function displays statistics on the total and average trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time} seconds")

    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function displays statistics on bikeshare users
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types_count = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types_count)

    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_count)
    else:
        print("\nGender information is not available for this dataset.")

    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]

        print("\nEarliest year of birth:", int(earliest_birth_year))
        print("Most recent year of birth:", int(most_recent_birth_year))
        print("Most common year of birth:", int(common_birth_year))
    else:
        print("\nBirth year information is not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Display raw data
def display_raw_data(df):
    print('\nDisplaying raw data...\n')
    start_loc = 0
    while True:
        view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no.\n')
        if view_data.lower() != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        more_data = input('Would you like to view more data? Enter yes or no.\n')
        if more_data.lower() != 'yes':
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('\nSummary of loaded data:\n')
        print(df.head())  # Display summary of loaded data

        display_raw_data(df)  # Offer to display raw data
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
