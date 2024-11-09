import requests

def get_air_quality(city_name, api_key):
    # First, get the latitude and longitude of the city
    location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    location_response = requests.get(location_url).json()

    if not location_response:
        print("City not found.")
        return

    # Extract latitude and longitude
    lat = location_response[0]['lat']
    lon = location_response[0]['lon']
    
    # Use coordinates to get air quality data
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    air_quality_response = requests.get(air_quality_url).json()

    # Parse and display air quality data
    air_data = air_quality_response.get("list", [])[0]
    if not air_data:
        print("No air quality data found.")
        return

    components = air_data["components"]
    aqi = air_data["main"]["aqi"]
    print(f"Air Quality in {city_name}:")
    print(f"AQI (Air Quality Index): {aqi} (1-Good, 5-Very Poor)")
    print(f"PM2.5: {components['pm2_5']} µg/m³")
    print(f"PM10: {components['pm10']} µg/m³")
    print(f"CO (Carbon Monoxide): {components['co']} µg/m³")
    print(f"NO (Nitrogen Monoxide): {components['no']} µg/m³")
    print(f"NO2 (Nitrogen Dioxide): {components['no2']} µg/m³")
    print(f"O3 (Ozone): {components['o3']} µg/m³")
    print(f"SO2 (Sulfur Dioxide): {components['so2']} µg/m³")

# Usage Example
api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
city_name = "Budapest"  # Replace with your chosen city
get_air_quality(city_name, api_key)
