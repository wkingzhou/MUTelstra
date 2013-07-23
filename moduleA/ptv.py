# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with PTV Website
# Renlord Y.
################################################################################
import urllib
import time

from HTMLParser import HTMLParser

# Important HTML Tags
LINK = "href"
TITLE = "title"

# Custom Omissions
blocked_urls = ["timetables/", "disruptions/", "tickets/myki/"]

# Keywords 
transport = ['trains', 'tram', 'buses']

# Regular Expressions

# Trains 
def mTrain(string):
    # train disruption keywords
    disruption = ['replacing', 'closed', 'delays', 'disrupted']
    
    # train line services
    tLines = ['cranbourne', 'pakenham', 'werribee', 'williamstown', \
        'sandringham', 'frankston', 'craigieburn', 'alamein', \
        'belgrave', 'lilydale', 'glen', 'waverley']

    # months
    months = ['january', 'february', 'march', 'april', 'may', 'june', \
                'july', 'august', 'september', 'october', 'november', \
                'december']
    
    #time keys
    time = ['am', 'pm']

    affected_lines = []

    words = string.split()

    for word in words:
        if word.strip(',').lower() in tLines:
            affected_lines.append(word)
        if 'am' in word or 'pm' in word:
            affected_time = word
        if ':' in word:
            n = string.index(word)
            break
    
    # DICTIONARY_TYPE
    affected_dates = dateHandler(string[n:])
    
    print affected_lines, affected_dates

# HTML Parser
class ptvHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        blocking = False
        if tag == "a" and attrs[0][0] == TITLE and attrs[1][0] == LINK:
            for url in blocked_urls:
                if url == attrs[1][1]:
                    blocking = True
                    break
            if not blocking:
                #TEMPORARY
                mTrain(attrs[0][1])
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        return


# Data Processing Function
"""
Function: build_output
PARAM:
  @ ptvdata, DICTIONARY data set.
  @ key, what is your data part of?
  @ data, concatenates your current data to lists of data existing for the given
          key.

RETURN:
  [currently] prints formated output according to what you have supplied.
"""
def build_output(ptvdata, key, data):
    while(True):
        try:
            ptvdata[key] = ptvdata[key].append(data)
            break
        except KeyError:
            ptvdata[key] = []  
    return

"""
dateHandler(string)
PARAM:
    @string, string TYPE only literal date formats.

RETURN:
    disruption dates @ DICT type
"""
def dateHandler(string):
    
    disruption_dates = {}
    
    months = ['january', 'february', 'march', 'april', 'may', 'june', \
                'july', 'august', 'september', 'october', 'november', \
                'december']

    # Types
    CONTINUOUS = 0
    DISCRETE = 1

    words = string.split()
    for word in words:
        try:
            word.strip(",")
            day = int(word)

        except ValueError:
            if word.lower() in months:
                if 'start' not in disruption_dates.keys():
                    disruption_dates['start'] = (day, word)
                else:
                    disruption_dates['end'] = (day, word)  
            else:
                if word == '-':
                    disruption_dates['type'] = CONTINUOUS
                if word == 'and':
                    disruption_dates['type'] = DISCRETE
                    
    return disruption_dates   
      
# Main Module
page = urllib.urlopen("http://ptv.vic.gov.au/disruptions/")
page = page.read()

parser = ptvHTMLParser()

ptvdata = {}

toggle_data = False

parser.feed(page)


# Tram
def tram():
    return
# Buses
def bus():
    return




