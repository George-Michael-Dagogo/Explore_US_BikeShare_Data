import time
import pandas as pd
import numpy as np
import streamlit as st
CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
st.title('WELCOME TO TEAM MATPLOTLIB')
st.header('A web application showing the Bikeshare project')
def check_input(input_str,input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read=st.text_iput(input_str)
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    st.write("Sorry, your input should be: chicago new york city or washington")
                if input_type == 2:
                    st.write("Sorry, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    st.write("Sorry, your input should be: sunday, ... friday, saturday or all")
        except ValueError:
            st.write("Sorry, your input is wrong")
    return input_read

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    st.write('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = st.text_input("Would you like to see the data for chicago, new york city or washington?").lower()
    # get user input for month (all, january, february, ... , june)
    month = st.text_input("Which Month (all, january, ... june)?").lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = st.text_input("Which day? (all, monday, tuesday, ... sunday)").lower()
    st.write('-'*40)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    st.write('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]

    st.write('Most Popular Month:', months[popular_month].title())

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    st.write('Most Day Of Week:', popular_day_of_week)

    # display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]

    st.write('Most Common Start Hour:', popular_common_start_hour)

    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    st.write('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    st.write('Most Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    st.write('Most End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    st.write('Most frequent combination of Start Station and End Station trip:\n', popular_combination_station)

    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    st.write('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    st.write('Total Travel Time:', total_travel_time,'seconds')
    #display highest trip duration
    highest_trip_duration = df['Trip Duration'].max()
    st.write('Highest travel time is:', highest_trip_duration,'seconds')
    #display lowest trip duration
    lowest_trip_duration = df['Trip Duration'].min()
    st.write('Lowest travel time is:', lowest_trip_duration,'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    st.write('Mean Travel Time:', mean_travel_time,'seconds')

    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    st.write('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    st.write('User Type Stats:')
    st.write(df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        st.write('Gender Stats:')
        st.write(df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        st.write('Birth Year Stats:')
        most_common_year = df['Birth Year'].mode()[0]
        st.write('Most Common Year:',most_common_year)
        most_recent_year = df['Birth Year'].max()
        st.write('Most Recent Year:',most_recent_year)
        earliest_year = df['Birth Year'].min()
        st.write('Earliest Year:',earliest_year)
    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)


#Def showraw data
def show_raw_data(df):
    

    
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    while True:
        raw_data = st.text_input('\nWould you like to see the first 5 rows of raw data? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            break
                
            
        else:
            st.write(df.head())
            next = 0
            while True:
            
                raw_data = st.text_input('\nWould you like to see the next five rows of raw data? Enter yes or no.\n')
                if raw_data.lower() == 'yes':
                    next += 5
                    st.write(df.iloc[next:next+5])
                    break
                
                if raw_data.lower()!= 'yes':
                    break
        
            break        
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_raw_data(df)
        break
        st.write('refresh the page to restart')

        #restart = st.text_input('\nWould you like to restart? Enter yes or no.\n')
        #if restart.lower() != 'yes':
         #   break


if __name__ == "__main__":
	main()
    
st.header('Refresh the page to restart or edit the values to see new data')