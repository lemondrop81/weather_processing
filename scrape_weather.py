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

    def handle_starttag(self, tag, attrs):
        """Checks which start tag gets opened."""
        if tag == 'tbody':
            self.tbodyTag = True
        if tag == 'tr':
            self.trTag = True
        if tag == 'td':
            self.tdTag = True

    def handle_endtag(self, tag):
        """Checks which end tag gets closed."""
        if tag == 'tbody':
            self.tbodyTag = False
        if tag == 'tr':
            self.trTag = False
        if tag == 'td':
            self.tdTag = False

    def handle_data(self, data):
        """Handles the data inbetween the tags and adds it to a dictionary"""
        if self.trTag == True and self.tbodyTag == True and self.tdTag == True:
            print(data)


myparser = WeatherScraper()

with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5') as response:
    html = str(response.read())

myparser.feed(html)