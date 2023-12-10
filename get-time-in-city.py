from datetime import datetime
import pytz

def get_time_in_city(city, user_time=None):
    # Get the current time in the user's timezone or use the provided time
    if user_time is None:
        user_time = datetime.now()
    else:
        user_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")

    # Define the timezone for the user's city
    try:
        city_timezone = pytz.timezone(city)
    except pytz.UnknownTimeZoneError:
        return f"Error: Timezone not found for {city}"

    # Convert the user's time to the city's timezone
    city_time = user_time.astimezone(city_timezone)

    return f"The current time in {city} is {city_time.strftime('%Y-%m-%d %H:%M:%S')}"

if __name__ == "__main__":
    # Get user input for city and time
    city_name = input("Enter the city name: ")
    user_input_time = input("Enter the time in the format 'YYYY-MM-DD HH:MM:SS' (Press Enter for current time): ")

    # Call the function to get the time in the specified city
    result = get_time_in_city(city_name, user_input_time)

    # Print the result
    print(result)
