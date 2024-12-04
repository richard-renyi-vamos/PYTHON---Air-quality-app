import requests
import tkinter as tk
from tkinter import messagebox

def get_air_quality(city_name, api_key):
    try:
        # Get the latitude and longitude of the city
        location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
        location_response = requests.get(location_url).json()

        if not location_response:
            messagebox.showerror("Error", "City not found. Please check the city name.")
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
            messagebox.showerror("Error", "No air quality data found.")
            return

        components = air_data["components"]
        aqi = air_data["main"]["aqi"]

        # Display air quality data in the GUI
        result = (
            f"Air Quality in {city_name}:\n"
            f"AQI (Air Quality Index): {aqi} (1-Good, 5-Very Poor)\n"
            f"PM2.5: {components['pm2_5']} µg/m³\n"
            f"PM10: {components['pm10']} µg/m³\n"
            f"CO (Carbon Monoxide): {components['co']} µg/m³\n"
            f"NO (Nitrogen Monoxide): {components['no']} µg/m³\n"
            f"NO2 (Nitrogen Dioxide): {components['no2']} µg/m³\n"
            f"O3 (Ozone): {components['o3']} µg/m³\n"
            f"SO2 (Sulfur Dioxide): {components['so2']} µg/m³\n"
        )
        result_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fetch_data():
    city_name = city_entry.get()
    if not city_name:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    get_air_quality(city_name, api_key)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Air Quality Checker")

# Input Section
city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=5)
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Check Air Quality", command=fetch_data)
fetch_button.pack(pady=10)

# Result Section
result_label = tk.Label(root, text="", justify="left", font=("Helvetica", 10))
result_label.pack(pady=10)

# Run the application
root.mainloop()
