from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations
"""
    Weather processing app
    April 11, 2022
    Description: A simple program to add user interface.
"""

class WeatherProcessor():
    """Contains the code for the user interface"""
    userSelection = input("Fetch all available weather data, update existing, or skip? ([F]ull/[U]pdate/[S]kip):")
    print(userSelection)