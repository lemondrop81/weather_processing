from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request
import calendar
from datetime import datetime

"""
    Weather processing app
    March 23, 2022
    Description: A simple program to scrape Winnipeg weather data
"""

class WeatherScraper(HTMLParser):

    def __init__(self):
        """Initialize the HTML Parser and initializes the variables."""
        HTMLParser.__init__(self)
        self.tbodyTag = False
        self.tdTag = False
        self.trTag = False
        self.aTag = False
        self.strongTag = False
        self.spanTag = False
        self.counter = 0
        self.daysInMonth = 0
        self.current = 0
        self.daily_temps = {}
        self.maxTemp = 0
        self.minTemp = 0
        self.meanTemp = 0



    def get_data(self):
        """Gets the data from the URL."""
        today = datetime.today()
        currentYear = today.year
        currentMonth = today.month
        self.daysInMonth = calendar.monthrange(2018, 3)[1]
        with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=3') as response:
            html = str(response.read())
        self.feed(html)

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

    def handle_endtag(self, tag):
        """Checks which end tag gets closed."""
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

    def handle_data(self, data):
        """Handles the data inbetween the tags and adds it to a dictionary"""
        if self.trTag == True and self.tbodyTag == True and self.spanTag == False and self.tdTag == True and self.aTag == False and self.counter < 3 and self.strongTag == False and self.current < self.daysInMonth:
            self.counter = self.counter + 1
            if self.counter == 3:
                self.current = self.current + 1
            if data == 'LegendM' or data == 'M' or data == 'E':
                data = ''            
            print(data)

        



myparser = WeatherScraper()

myparser.get_data()
