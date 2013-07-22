# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with VicRoads-VicTraffic Website
################################################################################
import urllib
import time

from HTMLParser import HTMLParser

# Important HTML Tags
#LINK = "href"
#TITLE = "title"

# Custom Omissions
#blocked_urls = ["timetables/", "disruptions/", "tickets/myki/"]

# Keywords 

# Regular Expressions

# HTML Parser
class victrafficHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "li":
            print attrs[0][1]

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        print data

# Data Processing Function
"""
Function: build_output
PARAM:
  @ victrafficdata, DICTIONARY data set.
  @ key, what is your data part of?
  @ data, concatenates your current data to lists of data existing for the given
          key.

RETURN:
  [currently] prints formated output according to what you have supplied.
"""
def build_output(victrafficdata, key, data):
  while(True):
    try:
      victrafficdata[key] = victrafficdata[key].append(data)
      break
    except KeyError:
      victrafficdata[key] = []  
      
# Main Module
page = urllib.urlopen("http://traffic.vicroads.vic.gov.au/nojs/")
page = page.read()

parser = victrafficHTMLParser()

victrafficdata = {}

toggle_data = False

parser.feed(page)
