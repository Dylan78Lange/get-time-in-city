import argparse
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

def capitalize_each_word(s):
    """Capitalize the first letter of each word in a string."""
    return ' '.join(word.capitalize() for word in s.split())

def get_time_in_city(city, user_time=None, debug=False):
    try:
        # Get the current time in the user's timezone or use the provided time
        if user_time is None or user_time.strip() == '':
            user_time = datetime.now()
            print(f"Using local time: {user_time.strftime('%Y-%m-%d %H:%M:%S')}")
        elif user_time.strip():  # Check if the provided time is a non-empty string
            user_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
            print(f"Using user-provided time: {user_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Validate the city name
        if not city:
            raise ValueError("City name cannot be empty")

        # Get the dynamically generated city time zones
        city_timezones = get_city_timezones()

        # Try to find the exact city name
        city_timezone = city_timezones.get(city.lower())

        # If not found, try to find a city that contains the input
        if city_timezone is None:
            matching_cities = [c for c in city_timezones.keys() if city.lower() in c]
            if len(matching_cities) == 1:
                city_timezone = city_timezones[matching_cities[0]]
            elif len(matching_cities) > 1:
                raise ValueError(f"Ambiguous city name. Matches: {matching_cities}")
            else:
                raise ValueError(f"Timezone not found for {city}")

        # Convert the user's time to the city's timezone
        city_time = user_time.astimezone(pytz.timezone(city_timezone))

        # Capitalize the first letter of each word in the city name
        formatted_city = capitalize_each_word(city)
        return f"The current time in {formatted_city} is {city_time.strftime('%Y-%m-%d %H:%M:%S')}"

    except ValueError as ve:
        return f"Error: {ve}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the current time in a specified city.")
    parser.add_argument("city", nargs='+', help="The name of the city.")
    parser.add_argument("--time", help="Specify the time in 'YYYY-MM-DD HH:MM:SS' format.")
    parser.add_argument("--debug", action="store_true", help="Show available time zones for debugging.")

    args = parser.parse_args()

    try:
        # Call the function to get the time in the specified city
        result = get_time_in_city(' '.join(args.city), args.time, debug=args.debug)

        # Print the result
        print(result)

    except ValueError as ve:
        print(f"Error: {ve}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
