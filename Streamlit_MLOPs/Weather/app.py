import streamlit as st
import requests
from datetime import datetime
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Skip if dotenv is not installed

# Get API key from environment variable or Streamlit secrets
def get_api_key():
    # First try to get from streamlit secrets
    if 'OPENWEATHER_API_KEY' in st.secrets:
        return st.secrets['OPENWEATHER_API_KEY']
    # Then try environment variable
    return os.getenv('OPENWEATHER_API_KEY')

API_KEY = get_api_key()
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def get_weather_data(city):
    if not API_KEY:
        st.error("API key not found. Please configure the OPENWEATHER_API_KEY in your environment.")
        return None
        
    params = {
        'q': city,
        'appid': API_KEY,
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def main():
    st.title("Weather Information App")
    
    # Add a city input textbox
    city = st.text_input("Enter City Name:")
    
    # Add temperature unit selection
    temp_unit = st.radio(
        "Select Temperature Unit",
        ('Celsius', 'Fahrenheit')
    )
    
    if city:
        weather_data = get_weather_data(city)
        
        if weather_data:
            # Create columns for layout
            col1, col2 = st.columns(2)
            
            # Basic weather information
            with col1:
                st.subheader("Current Weather")
                weather_desc = weather_data['weather'][0]['description'].title()
                st.write(f"**Condition:** {weather_desc}")
                
                temp_k = weather_data['main']['temp']
                if temp_unit == 'Celsius':
                    temp = round(kelvin_to_celsius(temp_k), 1)
                    unit = "°C"
                else:
                    temp = round(kelvin_to_fahrenheit(temp_k), 1)
                    unit = "°F"
                
                st.write(f"**Temperature:** {temp}{unit}")
                st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
                
            # Additional weather details
            with col2:
                st.subheader("Additional Info")
                
                wind_speed = weather_data['wind']['speed']
                st.write(f"**Wind Speed:** {wind_speed} m/s")
                
                if 'rain' in weather_data:
                    rain = weather_data['rain'].get('1h', 0)
                    st.write(f"**Rainfall (1h):** {rain} mm")
                
                pressure = weather_data['main']['pressure']
                st.write(f"**Pressure:** {pressure} hPa")
            
            # Sunrise and Sunset times
            st.subheader("Sun Times")
            col3, col4 = st.columns(2)
            
            with col3:
                sunrise_timestamp = weather_data['sys']['sunrise']
                sunrise_time = datetime.fromtimestamp(sunrise_timestamp)
                st.write(f"**Sunrise:** {sunrise_time.strftime('%H:%M')}")
            
            with col4:
                sunset_timestamp = weather_data['sys']['sunset']
                sunset_time = datetime.fromtimestamp(sunset_timestamp)
                st.write(f"**Sunset:** {sunset_time.strftime('%H:%M')}")
            
            # Location details
            st.subheader("Location Details")
            st.write(f"**Country:** {weather_data['sys']['country']}")
            st.write(f"**Coordinates:** Lat {weather_data['coord']['lat']}, Lon {weather_data['coord']['lon']}")

if __name__ == "__main__":
    main()