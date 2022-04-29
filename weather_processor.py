"""
    Weather processing app
    April 11, 2022
    Description: A simple program to add user interface.
"""
import logging
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor():
    """Contains the code for the user interface"""
    def __init__(self):
        """Class Constructor"""
        try:
            self.logger = logging.getLogger('Weather Processor')
            self.logger.setLevel(logging.DEBUG)
            # create file handler which logs even debug messages
            error_log = logging.FileHandler('error.log')
            error_log.setLevel(logging.DEBUG)
            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            error_log.setFormatter(formatter)
            # add the handlers to the logger
            self.logger.addHandler(error_log)
            user_selection = input("""Fetch all available weather data, update existing, or skip? ([F]ull/[U]pdate/[S]kip): """)
            if user_selection in ('F', 'f'):
                remove_data = DBOperations()
                remove_data.purge_data()

                myparser = WeatherScraper()
                myparser.get_data(0)

            if user_selection in ('U', 'u'):
                weather = DBOperations.fetch_data(self)

                myparser = WeatherScraper()
                myparser.get_data(weather)
            try:
                initial_year = input("Enter from year [YYYY]: ")
                final_year = input("Enter to year [YYYY]: ")

                if initial_year > final_year:
                    raise ValueError("WeatherProcessor:__init__:Intial year can't be larger then final year")
                weather = DBOperations.fetch_data(self, initial_year, final_year)
                PlotOperations.boxplot(self, weather, initial_year, final_year)
            except Exception as inst:
                self.logger.ERROR(inst)

            try:
                year = input("Enter year [YYYY]: ")
                month = input("Enter month [MM]: ")

                if year.isdigit() is False or month.isdigit() is False:
                    raise ValueError("WeatherProcessor:__init__: You did not enter a number")
                lineplot = DBOperations.fetch_data(self, 0, 0, year, month)
                PlotOperations.lineplot(self, lineplot)
            except Exception as inst:
                self.logger.ERROR(inst)

        except Exception as inst:
            self.logger.ERROR(inst)

if __name__ == "__main__":
    try:
        test = WeatherProcessor()
    except Exception as error:
        logging.debug(error)
