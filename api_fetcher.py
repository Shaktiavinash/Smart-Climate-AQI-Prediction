import requests # type: ignore

def fetch_weather_data(city_name):
    """Fetch current weather data using OpenWeatherMap API."""
    api_key = "1b5e09a1380f906d5a9da3caa9c734b9"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
