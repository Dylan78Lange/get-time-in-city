from datetime import datetime
import pytz

def get_city_timezones():
    """Dynamically fetch and return a dictionary of city names and their time zones."""
    city_timezones = {}
    for tz in pytz.all_timezones:
        # Extract the city name from the time zone
        parts = tz.split('/')
        if len(parts) > 1:
            city = parts[-1].replace('_', ' ')
            city_timezones[city.lower()] = tz
    return city_timezones

def get_time_in_city(city, user_time=None, debug=False):
    try:
        # Get the current time in the user's timezone or use the provided time
        if user_time is None or user_time.strip() == '':
            user_time = datetime.now()
            print(f"Using local time: {user_time.strftime('%Y-%m-%d %H:%M:%S')}")
        elif user_time.strip():  # Check if the provided time is a non-empty string
            user_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
            print(f"Using user-provided time: {user_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            raise ValueError("Invalid time format")

        # Print the list of available time zones for debugging
        if debug:
            print("Available time zones:")
            for tz in pytz.all_timezones:
                print(tz)

        # Validate the city name
        if not city:
            raise ValueError("City name cannot be empty")

        # Get the dynamically generated city time zones
        city_timezones = get_city_timezones()

        # Make the input city name case-insensitive
        city_lower = city.lower()

        # Define the timezone for the user's city using the mapping
        city_timezone = city_timezones.get(city_lower)
        if not city_timezone:
            raise ValueError(f"Timezone not found for {city}")

        # Convert the user's time to the city's timezone
        city_time = user_time.astimezone(pytz.timezone(city_timezone))

        return f"The current time in {city} is {city_time.strftime('%Y-%m-%d %H:%M:%S')}"

    except ValueError as ve:
        return f"Error: {ve}"

if __name__ == "__main__":
    try:
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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
