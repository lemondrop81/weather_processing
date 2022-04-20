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

import db_operations

class WeatherScraper(HTMLParser):
    """Contains database operations"""

    def __init__(self):
        """Initialize the HTML Parser and initializes the variables."""
        HTMLParser.__init__(self)
        self.tbody_tag = False
        self.td_tag = False
        self.tr_tag = False
        self.a_tag = False
        self.strong_tag = False
        self.span_tag = False
        self.title_tag = False
        self.counter = 0
        self.daysInMonth = 0
        self.currentMonth = 0
        self.currentYear = 0
        self.currentDay = 0
        self.month = 0
        self.current = 0
        self.daily_temps = {}
        self.weather = {}
        self.nextMonth = True
        self.latest = 0



    def get_data(self, latest):
        """Gets the data from the URL."""
        today = datetime.today()
        self.currentYear = today.year
        self.currentMonth = today.month
        self.latest = latest

        while self.nextMonth:
            self.month = calendar.month_name[self.currentMonth]
            #self.currentDay = today.day
            self.daysInMonth = calendar.monthrange(self.currentYear, self.currentMonth)[1]
            url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={self.currentYear}&Month={self.currentMonth}"
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
                print(url)
            self.feed(html)
            self.currentMonth = self.currentMonth - 1
            self.current = 0
            if self.currentMonth == 0:
                self.currentYear = self.currentYear - 1
                self.currentMonth = 12
        if self.latest == 0:
            db_operations.DBOperations.initialize(self)
        db_operations.DBOperations.save_data(self, self.weather)

    def handle_starttag(self, tag, attrs):
        """Checks which start tag gets opened."""
        if tag == 'tbody':
            self.tbody_tag = True
        if tag == 'tr':
            self.tr_tag = True
        if tag == 'td':
            self.td_tag = True
        if tag == 'a':
            for value in attrs:
                if 'legend' in value:
                    self.a_tag = False
                else:
                    self.a_tag = True
        if tag == 'strong':
            self.strong_tag = True
        if tag == 'span':
            self.span_tag = True
        if tag == 'title':
            self.title_tag = True

    def handle_endtag(self, tag):
        """Checks which end tag gets closed."""
        if self.nextMonth == False:
            return
        if tag == 'tbody':
            self.tbody_tag = False
        if tag == 'tr':
            self.tr_tag = False
            self.counter = 0
        if tag == 'td':
            self.td_tag = False
        if tag == 'a' :
            self.a_tag = False
        if tag == 'strong' :
            self.strong_tag = False
        if tag == 'span' :
            self.span_tag = False
        if tag == 'title' :
            self.title_tag = False

    def handle_data(self, data):
        """Handles the data inbetween the tags and adds it to a dictionary"""
        #Check the title tag to see if you reached the end
        if self.title_tag == True:
            if f"{self.month} {self.currentYear}" not in data:
                self.nextMonth = False
                return

        currentDate = f"{self.currentYear}-{self.currentMonth +1:02d}-{self.current:02d}"
        if self.latest != 0:
            str = ''.join(self.latest)
            if str > currentDate:
                self.nextMonth = False
                return

        if self.title_tag == True:
            if data in ('LegendM', 'M', 'E', '\\xa0'):
                self.tr_tag = False
                return

        #Check to see if you are getting the max, min or mean values
        if self.tr_tag == True and self.tbody_tag == True and self.span_tag == False and self.td_tag == True and self.a_tag == False and self.counter < 3 and self.strong_tag == False and self.current < self.daysInMonth:
            self.counter = self.counter + 1
            if self.counter == 3:
                self.current = self.current + 1

            today = datetime.today()
            currentYear = today.year
            currentMonth = today.month
            currentDay = today.day
            currentDate = f"{self.currentYear}-{self.currentMonth:02d}-{self.current:02d}"

            if currentYear == self.currentYear and currentMonth == self.currentMonth:
                if self.current < currentDay:
                    #Checks if the data is missing
                    if data in ('LegendM', 'M', 'E', '\\xa0'):
                        self.tr_tag = False
                        self.current = self.current + 1
                        return
                    #use modulus to see which data value you are assigning
                    if self.counter % 3 == 1:
                        self.daily_temps['Max'] = data
                    if self.counter % 3 == 2:
                        self.daily_temps['Min'] = data
                    if self.counter % 3 == 0:
                        self.daily_temps['Mean'] = data
                    if self.counter == 3:
                        #Deep copy to the dictionary
                        if self.latest == 0 or str < currentDate:
                            self.weather[currentDate] = copy.deepcopy(self.daily_temps)
            else:
                #Checks if the data is missing
                if data in ('LegendM', 'M', 'E', '\\xa0'):
                    self.tr_tag = False
                    self.current = self.current + 1
                    return
                #use modulus to see which data value you are assigning
                if self.counter % 3 == 1:
                    self.daily_temps['Max'] = data
                if self.counter % 3 == 2:
                    self.daily_temps['Min'] = data
                if self.counter % 3 == 0:
                    self.daily_temps['Mean'] = data
                if self.counter == 3:
                    #Deep copy to the dictionary
                    if self.latest == 0 or str < currentDate:
                        self.weather[currentDate] = copy.deepcopy(self.daily_temps)
