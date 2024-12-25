import requests
import tkinter as tk
from tkinter import messagebox
from tkinterweb import HtmlFrame  # To embed the map in Tkinter
import folium

# Function to fetch air quality data
def get_air_quality(lat, lon, api_key):
    try:
        # Fetch air quality data using latitude and longitude
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
            f"Air Quality at Coordinates ({lat}, {lon}):\n"
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

# Function to create a zoomable Earth map
def create_map():
    global map_widget
    # Create a Folium map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add a click event to capture latitude and longitude
    m.add_child(folium.ClickForMarker(popup="Selected Location"))

    # Save the map to an HTML file
    map_file = "map.html"
    m.save(map_file)

    # Load the map into the HTML frame
    map_widget.load_url(map_file)

# Function to fetch data based on the selected coordinates
def fetch_data():
    try:
        coordinates = map_widget.get_url()  # Get the clicked coordinates from the map
        if "marker" not in coordinates:
            messagebox.showwarning("Input Error", "Please select a location on the map.")
            return

        # Extract latitude and longitude from the URL
        coords = coordinates.split("marker=")[-1].split(",")
        lat, lon = float(coords[0]), float(coords[1])
        api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
        get_air_quality(lat, lon, api_key)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Air Quality Checker with Map")

# Map Section
map_widget = HtmlFrame(root, width=800, height=600)
map_widget.pack(pady=5)
create_map()

# Fetch Button
fetch_button = tk.Button(root, text="Check Air Quality", command=fetch_data)
fetch_button.pack(pady=10)

# Result Section
result_label = tk.Label(root, text="", justify="left", font=("Helvetica", 10))
result_label.pack(pady=10)

# Run the application
root.mainloop()  
