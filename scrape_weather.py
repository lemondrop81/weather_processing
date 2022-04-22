from asyncio.windows_events import NULL
from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request
import calendar
from datetime import datetime
import copy
import logging
import db_operations

"""
    Weather processing app
    March 23, 2022
    Description: A simple program to scrape Winnipeg weather data
"""

class WeatherScraper(HTMLParser):
    
    def __init__(self):
        """Initialize the HTML Parser and initializes the variables."""
        try:
            HTMLParser.__init__(self)
            logger = logging.getLogger("PlotOperations:" + __name__)
            self.tbodyTag = False
            self.tdTag = False
            self.trTag = False
            self.aTag = False
            self.strongTag = False
            self.spanTag = False
            self.titleTag = False
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
        except Exception as exception:
            self.logger.INFO("WeatherScraper:__init__:", exception)



    def get_data(self, latest):
        """Gets the data from the URL."""
        try:
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
        except Exception as exception:
            self.logger.INFO("WeatherScraper:get_data:", exception)

    def handle_starttag(self, tag, attrs):
        """Checks which start tag gets opened."""
        if tag == 'tbody':
            self.tbodyTag = True        
        if tag == 'tr':
            self.trTag = True
        if tag == 'td':
            self.tdTag = True
        if(tag == 'a'):
            for name, value in attrs:
                if 'legend' in value:
                    self.aTag = False
                else:
                    self.aTag = True
        if(tag == 'strong'):
            self.strongTag = True
        if(tag == 'span'):
            self.spanTag = True
        if(tag == 'title'):
            self.titleTag = True

    def handle_endtag(self, tag):
        """Checks which end tag gets closed."""
        if self.nextMonth == False:
            return
        if tag == 'tbody':
            self.tbodyTag = False
        if tag == 'tr':
            self.trTag = False
            self.counter = 0
        if tag == 'td':
            self.tdTag = False
        if(tag == 'a'):
            self.aTag = False
        if(tag == 'strong'):
            self.strongTag = False
        if(tag == 'span'):
            self.spanTag = False
        if(tag == 'title'):
            self.titleTag = False

    def handle_data(self, data):
        """Handles the data inbetween the tags and adds it to a dictionary"""
        #Check the title tag to see if you reached the end
        if self.titleTag == True:
            if f"{self.month} {self.currentYear}" not in data:
                self.nextMonth = False
                return

        currentDate = f"{self.currentYear}-{self.currentMonth +1:02d}-{self.current:02d}"
        if self.latest != 0:
            str = ''.join(self.latest)
            if str > currentDate:
                self.nextMonth = False
                return
        

        if self.titleTag == True:
            if 'Avg' in data or 'Xtrm' in data or 'Sum' in data:
                self.trTag = False
                return

        #Check to see if you are getting the max, min or mean values
        if self.trTag == True and self.tbodyTag == True and self.spanTag == False and self.tdTag == True and self.aTag == False and self.counter < 3 and self.strongTag == False and self.current < self.daysInMonth:
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
                    if data == 'LegendM' or data == 'M' or data == 'E' or data == "\xa0":
                        self.trTag = False
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
                        if self.latest == 0 or str < currentDate:
                            self.weather[currentDate] = copy.deepcopy(self.daily_temps)
            else:
                #Checks if the data is missing
                if data == 'LegendM' or data == 'M' or data == 'E' or data == "\xa0":
                    self.trTag = False
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
                    if self.latest == 0 or str < currentDate:
                        self.weather[currentDate] = copy.deepcopy(self.daily_temps)