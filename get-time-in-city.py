from datetime import datetime
import pytz

# Mapping of common city names to time zones
city_timezones = {
    'Paris': 'Europe/Paris',
    'Los_Angeles': 'America/Los_Angeles',
    'Johannesburg': 'Africa/Johannesburg',
    # Add more cities as needed
}

def get_time_in_city(city, user_time=None, debug=False):
    # Get the current time in the user's timezone or use the provided time
    if user_time is None or user_time.strip() == '':
        user_time = datetime.now()
        print(f"Using local time: {user_time.strftime('%Y-%m-%d %H:%M:%S')}")
    elif user_time.strip():  # Check if the provided time is a non-empty string
        user_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
        print(f"Using user-provided time: {user_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        return "Error: Invalid time format"

    # Print the list of available time zones for debugging
    if debug:
        print("Available time zones:")
        for tz in pytz.all_timezones:
            print(tz)

    # Define the timezone for the user's city using the mapping
    city_timezone = city_timezones.get(city)
    if not city_timezone:
        return f"Error: Timezone not found for {city}"

    # Convert the user's time to the city's timezone
    city_time = user_time.astimezone(pytz.timezone(city_timezone))

    return f"The current time in {city} is {city_time.strftime('%Y-%m-%d %H:%M:%S')}"

if __name__ == "__main__":
    # Get user input for time
    user_input_time = input("Enter the time in the format 'YYYY-MM-DD HH:MM:SS' (Press Enter for current time): ")

    # Set the default city to "Johannesburg"
    city_name = input(f"Enter the city name (default is Johannesburg): ") or "Johannesburg"

    # Ask the user if debugging information should be shown
    debug_toggle = input("Show available time zones for debugging? (yes/no, default is no): ").lower()
    debug = debug_toggle == 'yes'

    # Call the function to get the time in the specified city
    result = get_time_in_city(city_name, user_input_time, debug=debug)

    # Print the result
    print(result)
