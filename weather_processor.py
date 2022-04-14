from asyncio.windows_events import NULL
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
    def __init__(self):
        """Constructor"""
        userSelection = input("Fetch all available weather data, update existing, or skip? ([F]ull/[U]pdate/[S]kip): ")
        
        if userSelection == 'F' or userSelection == 'f':
            removeData = DBOperations()
            removeData.purge_data()

            myparser = WeatherScraper()
            myparser.get_data(0)

        if userSelection == 'U' or userSelection == 'u':
            weather = DBOperations.fetch_data(self,  NULL, NULL,  NULL, NULL)

            myparser = WeatherScraper()
            myparser.get_data(weather)
        
        initialYear = input("Enter from year [YYYY]: ")
        finalYear = input("Enter to year [YYYY]: ")

        weather = DBOperations.fetch_data(self, initialYear, finalYear)
        PlotOperations.boxplot(self, weather, initialYear, finalYear)

        year = input("Enter year [YYYY]: ")
        month = input("Enter month [MM]: ")

        lineplot = DBOperations.fetch_data(self, NULL, NULL, year, month)
        PlotOperations.lineplot(self, lineplot)
        exit()

myparser = WeatherProcessor()