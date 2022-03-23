from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request

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
        self.counter = 0

    def handle_starttag(self, tag, attrs):
        """Checks which start tag gets opened."""
        if tag == 'tbody':
            self.tbodyTag = True
        if tag == 'tr':
            self.trTag = True
        if tag == 'td':
            self.tdTag = True
        if(tag == 'a'):
            self.aTag = True
        if(tag == 'strong'):
            self.strongTag = True

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

    def handle_data(self, data):
        """Handles the data inbetween the tags and adds it to a dictionary"""
        if self.trTag == True and self.tbodyTag == True and self.tdTag == True and self.aTag == False and self.counter < 3 and self.strongTag == False:
            print(data)
            self.counter = self.counter + 1
        



myparser = WeatherScraper()

with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=6') as response:
    html = str(response.read())

myparser.feed(html)