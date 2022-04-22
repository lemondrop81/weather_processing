"""
    Weather processing app
    March 23, 2022
    Description: A simple program to scrape Winnipeg weather data
"""
from html.parser import HTMLParser
import urllib.request
import calendar
from datetime import datetime
import copy
import logging
import db_operations


class WeatherScraper(HTMLParser):
    """Class to scrape the weather"""

    def __init__(self):
        """Initialize the HTML Parser and initializes the variables."""
        try:
            HTMLParser.__init__(self)
            self.logger = logging.getLogger("PlotOperations:" + __name__)
            self.tbody_tag = False
            self.td_tag = False
            self.tr_tag = False
            self.a_tag = False
            self.strong_tag = False
            self.span_tag = False
            self.title_tag = False
            self.counter = 0
            self.days_in_month = 0
            self.current_month = 0
            self.current_year = 0
            self.current_day = 0
            self.month = 0
            self.current = 0
            self.daily_temps = {}
            self.weather = {}
            self.next_month = True
            self.latest = 0
        except Exception as exception:
            self.logger.INFO("WeatherScraper:__init__:", exception)



    def get_data(self, latest):
        """Gets the data from the URL."""
        try:
            today = datetime.today()
            self.current_year = today.year
            self.current_month = today.month
            self.latest = latest

            while self.next_month:
                try:
                    self.month = calendar.month_name[self.current_month]
                    #self.current_day = today.day
                    self.days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]
                    url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={self.current_year}&Month={self.current_month}"
                    with urllib.request.urlopen(url) as response:
                        html = str(response.read())
                        print(url)
                    self.feed(html)
                    self.current_month = self.current_month - 1
                    self.current = 0

                    if self.current_month == 0:
                        self.current_year = self.current_year - 1
                        self.current_month = 12
                except Exception as exception:
                    self.logger.INFO("WeatherScraper:get_data:while:", exception)
            if self.latest == 0:
                db_operations.DBOperations.initialize(self)
            db_operations.DBOperations.save_data(self, self.weather)
        except Exception as exception:
            self.logger.INFO("WeatherScraper:get_data:", exception)

    def handle_starttag(self, tag, attrs):
        """Checks which start tag gets opened."""
        try:
            if tag == 'tbody':
                self.tbody_tag = True
            if tag == 'tr':
                self.tr_tag = True
            if tag == 'td':
                self.td_tag = True
            if(tag == 'a'):
                for value in attrs:
                    if 'legend' in value:
                        self.a_tag = False
                    else:
                        self.a_tag = True
            if(tag == 'strong'):
                self.strong_tag = True
            if(tag == 'span'):
                self.span_tag = True
            if(tag == 'title'):
                self.title_tag = True
        except Exception as exception:
            self.logger.INFO("WeatherScraper:get_data:", exception)

    def handle_endtag(self, tag):
        """Checks which end tag gets closed."""
        try:
            if self.next_month == False:
                return
            if tag == 'tbody':
                self.tbody_tag = False
            if tag == 'tr':
                self.tr_tag = False
                self.counter = 0
            if tag == 'td':
                self.td_tag = False
            if(tag == 'a'):
                self.a_tag = False
            if(tag == 'strong'):
                self.strong_tag = False
            if(tag == 'span'):
                self.span_tag = False
            if(tag == 'title'):
                self.title_tag = False
        except Exception as exception:
            self.logger.INFO("WeatherScraper:get_data:", exception)

    def handle_data(self, data):
        """Handles the data inbetween the tags and adds it to a dictionary"""
        try:
            try:
                #Check the title tag to see if you reached the end
                if self.title_tag == True:
                    if f"{self.month} {self.current_year}" not in data:
                        self.next_month = False
                        return
            except ValueError:
                self.logger.INFO("WeatherScraper:handle_data:end")

            try:
                current_date = f"{self.current_year}-{self.current_month +1:02d}-{self.current:02d}"
                if self.latest != 0:
                    current= ''.join(self.latest)
                    if current> current_date:
                        self.next_month = False
                        return
            except ValueError:
                self.logger.INFO("WeatherScraper:handle_data:end")

            try:
                if self.title_tag == True:
                    if 'Avg' in data or 'Xtrm' in data or 'Sum' in data:
                        self.tr_tag = False
                        return
            except ValueError:
                self.logger.INFO("WeatherScraper:handle_data:avg/xtrm/sum")

            try:
                #Check to see if you are getting the max, min or mean values
                if self.tr_tag == True and self.tbody_tag == True and self.span_tag == False and self.td_tag == True and self.a_tag == False and self.counter < 3 and self.strong_tag == False and self.current < self.days_in_month:
                    self.counter = self.counter + 1

                    if self.counter == 3:
                        self.current = self.current + 1

                    today = datetime.today()
                    current_year = today.year
                    current_month = today.month
                    current_day = today.day
                    current_date = f"{self.current_year}-{self.current_month:02d}-{self.current:02d}"
            except ValueError:
                self.logger.INFO("WeatherScraper:handle_data:max/min or mean values")
            try:
                if current_year == self.current_year and current_month == self.current_month:
                    if self.current < current_day:
                        #Checks if the data is missing
                        if data == 'LegendM' or data == 'M' or data == 'E' or data == "\xa0":
                            self.tr_tag = False
                            self.current = self.current + 1
                            return
                        #use modulus to see which data value you are assigning
                        if (self.counter % 3) == 1:
                            self.daily_temps['Max'] = data
                        if (self.counter % 3) == 2:
                            self.daily_temps['Min'] = data
                        if (self.counter % 3) == 0:
                            self.daily_temps['Mean'] = data
                        if self.counter == 3:
                            #Deep copy to the dictionary
                            if self.latest == 0 or current< current_date:
                                self.weather[current_date] = copy.deepcopy(self.daily_temps)
            except ValueError:
                self.logger.INFO("WeatherScraper:handle_data:Update")
            else:
                #Checks if the data is missing
                if data == 'LegendM' or data == 'M' or data == 'E' or data == "\xa0":
                    self.tr_tag = False
                    self.current = self.current + 1
                    return
                #use modulus to see which data value you are assigning
                if (self.counter % 3) == 1:
                    self.daily_temps['Max'] = data
                if (self.counter % 3) == 2:
                    self.daily_temps['Min'] = data
                if (self.counter % 3) == 0:
                    self.daily_temps['Mean'] = data
                if self.counter == 3:
                    #Deep copy to the dictionary
                    if self.latest == 0 or current< current_date:
                        self.weather[current_date] = copy.deepcopy(self.daily_temps)
        except Exception as exception:
            self.logger.INFO("WeatherScraper:handle_data:", exception)
