"""
    Weather processing app
    April 11, 2022
    Description: A simple program to add user interface.
"""
from asyncio.windows_events import NULL
import logging
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor():
    """Contains the code for the user interface"""
    
    def __init__(self):
        """Class Constructor"""
        try:
            logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='spam.log',
                    filemode='a')
            user_selection = input("""Fetch all available weather data, update existing, or skip? ([F]ull/[U]pdate/[S]kip): """)
            if user_selection in ('F', 'f'):
                remove_data = DBOperations()
                remove_data.purge_data()

                myparser = WeatherScraper()
                myparser.get_data(0)

            if user_selection in ('U', 'u'):
                weather = DBOperations.fetch_data(self,  NULL, NULL,  NULL, NULL)

                myparser = WeatherScraper()
                myparser.get_data(weather)
            try:
                initial_year = input("Enter from year [YYYY]: ")
                final_year = input("Enter to year [YYYY]: ")

                if initial_year > final_year:
                    raise ValueError("WeatherProcessor:__init__: Intial year can't be larger then final year")
                weather = DBOperations.fetch_data(self, initial_year, final_year)
                PlotOperations.boxplot(self, weather, initial_year, final_year)
            except Exception as inst:
                logging.INFO(inst)

            try:
                year = input("Enter year [YYYY]: ")
                month = input("Enter month [MM]: ")
                int(year)
                int(month)
                
                lineplot = DBOperations.fetch_data(self, NULL, NULL, year, month)
                PlotOperations.lineplot(self, lineplot)
            except ValueError:
                logging.INFO("WeatherProcessor:__init__: You did not enter a number")

        except Exception as inst:
            logging.INFO(inst)

if __name__ == "__main__":
    try:
        test = WeatherProcessor()
    except Exception as error:
        logging.INFO(error)
