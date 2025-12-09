import requests
from typing import Tuple
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime
from zoneinfo import ZoneInfo

DEFAULT_LOCATION = "New York"
DEFAULT_TIMEZONE = "America/New_York"

#given a location string, returns the latitude, longitude, and address
def get_location_details(location: str = DEFAULT_LOCATION) -> Tuple[str,str,str]:
     # Geocode an address
        geolocator = Nominatim(user_agent="cli-dashboard")
        location_data = geolocator.geocode(location)
        return (location_data.latitude, location_data.longitude, location_data.address)

#given a location string, returns the temperature in F, current weather conditions, and city
def get_weather_details(location: str = DEFAULT_LOCATION) -> Tuple[int,str,str]:
        # Geocode an address
        location_data = get_location_details(location)

        if location_data is None:
            return (None,None,None)
        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={location_data[0]}&longitude={location_data[1]}&current_weather=true"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            cw = data.get("current_weather", {})
            temperature = cw.get("temperature")  # in Celsius by default

            # convert to Fahrenheit
            temp_f = int(temperature * 9/5 + 32) if temperature is not None else None

            weather_code = cw.get("weathercode")
            weather_conditions = _map_weather_code(weather_code)

            city = str(location_data[2]).split(",")[0]
            return (temp_f, weather_conditions, city)

#given a meteo weather code, returns the cooresponding weather conditions
def _map_weather_code(code: int) -> str:
        """Map Open-Meteo weather codes to emojis."""
        mapping = {
            0: "Clear",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return mapping.get(code, "Unknown Weather")

def get_timezone(latitude: float, longitude: float) -> ZoneInfo:
      
    # Initialize the TimezoneFinder object
    tf = TimezoneFinder()

    # Get the timezone string
    timezone_str = tf.certain_timezone_at(lat=latitude, lng=longitude)

    if timezone_str is None:
        return None
    else:
        print(f"The timezone for ({latitude}, {longitude}) is: {timezone_str}")
        return ZoneInfo(timezone_str)

