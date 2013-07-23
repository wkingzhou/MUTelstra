# -*- coding: utf-8 -*- 
#
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

# Global Var.
months = ['january', 'february', 'march', 'april', 'may', 'june', \
          'july', 'august', 'september', 'october', 'november', 'december']
          
parserToggle = False
          
# Housekeeping Function
def housekeeping(string):
    'transforms string into list of words in lower case and free of puncs.'
    words = string.split()
    for i in range(len(words)):
        words[i] = words[i].strip(',').lower()
    return words

# Trains 
def mTrain(string):
    # train disruption keywords
    disruption = ['replacing', 'closed', 'delays', 'disrupted']
    
    # train line services
    tLines = ['cranbourne', 'pakenham', 'werribee', 'williamstown', \
        'sandringham', 'frankston', 'craigieburn', 'alamein', \
        'belgrave', 'lilydale', 'glen', 'waverley']
    
    #time keys
    time = ['am', 'pm']

    affected_lines = []

    words = string.split()

    for word in words:
        if word.strip(',').lower() in tLines:
            affected_lines.append(word.strip(','))
        
        if 'am' in word or 'pm' in word:
            affected_time = word
            
        if ':' in word:
            n = string.index(word)
            break
    
    # Special Case: Glen Waverley processing.
    if 'Glen' in affected_lines:
        correction = affected_lines.index('Glen')
        affected_lines[correction] = 'Glen Waverley'
        affected_lines.remove('Waverley')
        
    # DICTIONARY_TYPE
    affected_dates = dateHandler(string[n:])
    
    print affected_lines
    print affected_dates

# Tram
def mTram(string):
    return
# Buses
def mBus(string):
    return
# Regional Trains
def rTrain(string):
    return

# HTML Parser
class ptvHTMLParser(HTMLParser):

    toggle_mode = 0
    parserToggle = False
    
    toggle_mode = 'DEFAULT'
    
    def handle_starttag(self, tag, attrs):
        blocking = False
        if tag == 'th':
            ptvHTMLParser.parserToggle = True
        else:
            ptvHTMLParser.parserToggle = False
            
        if tag == "a" and attrs[0][0] == TITLE and attrs[1][0] == LINK:
            for url in blocked_urls:
                if url == attrs[1][1]:
                    blocking = True
                    break

            if not blocking:   
                if ptvHTMLParser.toggle_mode == 'MTRAIN':
                    mTrain(attrs[0][1])
                elif ptvHTMLParser.toggle_mode == 'MTRAM':
                    mTram(attrs[0][1])
                elif ptvHTMLParser.toggle_mode == 'MBUS':
                    mBus(attrs[0][1])
                elif ptvHTMLParser.toggle_mode == 'RTRAIN':
                    rTrain(attrs[0][1])
                
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        if ptvHTMLParser.parserToggle == True and \
        data.lower() == 'metropolitan trains':
            ptvHTMLParser.toggle_mode = 'MTRAIN'
        elif data.lower() == 'metropolitan trams':
            ptvHTMLParser.toggle_mode = 'MTRAM'
        elif data.lower() == 'metropolitan buses':
            ptvHTMLParser.toggle_mode = 'MBUS'
        elif data.lower() == 'regional trains':
            ptvHTMLParser.toggle_mode = 'RTRAIN'
        
        return

# Data Processing Function
def dateHandler(string):
    'identifies from - to dates from string literal'
    disruption_dates = {}
    
    words = housekeeping(string)
        
    for word in words:
        try:
            day = int(word)
        except ValueError:
            if word in months:
                if 'start' not in disruption_dates.keys():
                    disruption_dates['start'] = (day, word.upper())
                else:
                    disruption_dates['end'] = (day, word.upper())  
            else:
                if word == '-' or word == '–': 
                    disruption_dates['type'] = 'CONTINUOUS'
                if word == 'and':
                    disruption_dates['type'] = 'DISCRETE'
    if 'end' not in disruption_dates.keys():
        disruption_dates['type'] = 'INDEFINITE'
               
    return disruption_dates   
      
# Main Module
page = urllib.urlopen("http://ptv.vic.gov.au/disruptions/")
page = page.read()

parser = ptvHTMLParser()

ptvdata = {}

toggle_data = False

parser.feed(page)


# Tram
def mTram():
    return
# Buses
def mBus():
    return




