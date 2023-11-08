import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Get user input for city, month, and day, and handle invalid inputs with while loops.

    Returns:
        tuple: A tuple containing the user's validated inputs for city, month, and day.
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city, handle invalid inputs with a while loop
    while True:
        city = input(
            "Enter the name of the city (chicago, new york city, washington): "
        )
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name. Please choose from the available options.")

    # Get user input for month and day, allow "all" as an option
    while True:
        month = input(
            'Enter the name of the month to filter by (e.g., january, february, ...), or "all" for no filter: '
        )
        month = month.lower()
        if month in ["all", "january", "february", "march", "april", "may", "june"]:
            break
        else:
            print('Invalid month name. Please enter a valid month or "all".')

    while True:
        day = input(
            'Enter the name of the day of the week to filter by (e.g., monday, tuesday, ...), or "all" for no filter: '
        )
        day = day.lower()
        if day in [
            "all",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]:
            break
        else:
            print('Invalid day name. Please enter a valid day or "all".')

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Load and filter bikeshare data for a specified city, month, and day.

    Args:
        city (str): The name of the city (chicago, new york city, washington).
        month (str): The name of the month to filter by ('all' or month name).
        day (str): The name of the day of the week to filter by ('all' or day name).

    Returns:
        pd.DataFrame: A Pandas DataFrame containing filtered bikeshare data.
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of the week
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # Apply filters for month and day
    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df["month"] == month]

    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """
    Calculate and display statistics on the most frequent times of travel.

    Args:
        df (pd.DataFrame): The DataFrame containing bikeshare data.

    Returns:
        None: Prints time stats Results
    """
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Display the most common month
    common_month = df["month"].mode()[0]
    print(f"The most common month is: {int(common_month)}")

    # Display the most common day of the week
    common_day = df["day_of_week"].mode()[0]
    print(f"The most common day of the week is: {common_day}")

    # Display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_start_hour = df["hour"].mode()[0]
    print(f"The most common start hour is: {common_start_hour}")

    print("\nThis took %s seconds." % round(time.time() - start_time, 1))
    print("-" * 40)


def station_stats(df):
    """
    Calculate and display statistics on the most popular stations and trips.

    Args:
        df (pd.DataFrame): The DataFrame containing bikeshare data.

    Returns:
        None: Prints station stats Results
    """
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df["Start-End Combination"] = df["Start Station"] + " to " + df["End Station"]
    common_combination = df["Start-End Combination"].mode()[0]
    print(
        f"The most frequent combination of start station and end station trip is: {common_combination}"
    )

    print("\nThis took %s seconds." % round(time.time() - start_time, 1))
    print("-" * 40)


def trip_duration_stats(df):
    """
    Calculate and display statistics on the total and average trip duration.

    Args:
        df (pd.DataFrame): The DataFrame containing bikeshare data.

    Returns:
        None: Prints trip duration statistics Results
    """
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time in minutes
    total_travel_time = df["Trip Duration"].sum()
    print(f"Total travel time: {round(total_travel_time / 60, 1)} minutes")

    # Display mean travel time in minutes
    mean_travel_time = df["Trip Duration"].mean()
    print(f"Mean travel time: {round(mean_travel_time / 60, 1)} minutes")

    print("\nThis took %s seconds." % round(time.time() - start_time, 1))
    print("-" * 40)


def user_stats(df):
    """
    Calculate and display statistics on bikeshare users, including user types, gender, and birth year.

    Args:
        df (pd.DataFrame): The DataFrame containing bikeshare data.

    Returns:
        None: Prints user statistics Results
    """
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df["User Type"].value_counts()
    print(f"Counts of user types:\n{user_type_counts}")

    # Display counts of gender if available in the dataset
    if "Gender" in df:
        gender_counts = df["Gender"].value_counts()
        print(f"Counts of gender:\n{gender_counts}")
    else:
        print("Gender information is not available for this dataset.")

    # Display earliest, most recent, and most common year of birth if available in the dataset
    if "Birth Year" in df:
        earliest_birth_year = int(df["Birth Year"].min())
        most_recent_birth_year = int(df["Birth Year"].max())
        common_birth_year = int(df["Birth Year"].mode()[0])
        print(f"Earliest birth year: {earliest_birth_year}")
        print(f"Most recent birth year: {most_recent_birth_year}")
        print(f"Most common birth year: {common_birth_year}")
    else:
        print("Birth year information is not available for this dataset.")

    print("\nThis took %s seconds." % round(time.time() - start_time, 1))
    print("-" * 40)

    
def display_raw_data(df):
    """
    Display raw data to the user in chunks of 5 rows at a time.

    Args:
        df (pd.DataFrame): The DataFrame containing bikeshare data.
    """
    i = 0
    raw = input('\nWould you like to see the raw data? Enter yes or no.\n').lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5])
            i += 5
            raw = input('\nWould you like to see 5 more rows of raw data? Enter yes or no.\n').lower()
        else:
            raw = input('\nYour input is invalid. Please enter only "yes" or "no".\n').lower()

def main():
    """
    Main function to interactively analyze bikeshare data.

    The function continuously prompts the user for inputs to filter data by city, month, and day.
    It then displays statistics on the most frequent times of travel, popular stations and trips,
    trip duration, and user statistics. The user can choose to restart the analysis or exit.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                return
            else:
                print('Invalid input. Please enter "yes" or "no".')

if __name__ == "__main__":
    main()


