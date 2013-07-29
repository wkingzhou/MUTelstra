# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with VicRoads-VicTraffic Website
# by yschin (July 2013)
################################################################################
import urllib

from HTMLParser import HTMLParser

# Initialise dictionary that can be used to pass data to calling functions
dictofdicts = {}  # Variable for dictionary of traffic alerts

# HTML Parser
class victrafficHTMLParser(HTMLParser):

    # initialise variables
    mode = 'DEFAULT'  # variable used for data classification
    datalevel = 0     # counter to keep track of data level
    location = ''     # location of traffic alert
    area = ''         # 2nd-level location for traffic alert (suburb etc)
    lfrom = ''        # road traffic incident applies from
    lto = ''          # road traffic incident applies to
    lnear = ''        # landmark traffic incident is near
    info1 = ''        # Type of traffic alert
    info2 = ''        # Additional description of traffic alert
    info3 = ''        # Further information on traffic alert
    start = ''        # Date/time traffic alert started
    updated = ''      # Date/time traffic alert last updated
    index = 0         # Index for dictionary of traffic alerts

    def handle_starttag(self, tag, attrs):
        if tag == "li": # tag that indicates start of useful data

            #print "\n", str.upper(attrs[0][1]) #temporary output for debugging

            if str.upper(attrs[0][1]) == 'ALERT': #for data classification
                victrafficHTMLParser.mode = 'ALERT'
            elif str.upper(attrs[0][1]) == 'ROADWORKS':
                victrafficHTMLParser.mode = 'ROADWORKS'
            elif str.upper(attrs[0][1]) == 'EMERGENCY':
                victrafficHTMLParser.mode = 'EMERGENCY'
            else:
                victrafficHTMLParser.mode = 'DEFAULT'

    def handle_data(self, data):
        if ("=" in data): #to remove nonsense data
            return
        elif str.strip(data): #to remove whitespace

            #print data #temporary output for debugging purposes

            # if-elif below to sort data into relevant categories
            # datalevel used as data structure is inconsistent
            if victrafficHTMLParser.datalevel == 0:
                victrafficHTMLParser.location = '' #initialise for next round
                victrafficHTMLParser.area = ''
                victrafficHTMLParser.lfrom = ''
                victrafficHTMLParser.lto = ''
                victrafficHTMLParser.lnear = ''
                victrafficHTMLParser.info1 = ''
                victrafficHTMLParser.info2 = ''
                victrafficHTMLParser.info3 = ''
                victrafficHTMLParser.start = ''
                victrafficHTMLParser.updated = ''
                victrafficHTMLParser.index += 1
                victrafficHTMLParser.location = str.lstrip(data)
                victrafficHTMLParser.datalevel = 1
            elif data == 'From:':
                victrafficHTMLParser.datalevel = 3
            elif victrafficHTMLParser.datalevel == 3:
                victrafficHTMLParser.lfrom = str.lstrip(data)
                victrafficHTMLParser.datalevel = 4
            elif data == 'To:':
                victrafficHTMLParser.datalevel = 4
            elif victrafficHTMLParser.datalevel == 4:
                victrafficHTMLParser.lto = str.lstrip(data)
                victrafficHTMLParser.datalevel = 6
            elif data == 'Near:':
                victrafficHTMLParser.datalevel = 5
            elif victrafficHTMLParser.datalevel == 5:
                victrafficHTMLParser.lnear = str.lstrip(data)
                victrafficHTMLParser.datalevel = 6
            elif victrafficHTMLParser.datalevel == 1:
                victrafficHTMLParser.area = str.lstrip(data)
                victrafficHTMLParser.datalevel = 2
            elif victrafficHTMLParser.datalevel == 6:
                victrafficHTMLParser.info1 = str.lstrip(data)
                victrafficHTMLParser.datalevel = 7
            elif victrafficHTMLParser.datalevel == 7:
                victrafficHTMLParser.info2 = str.lstrip(data)
                victrafficHTMLParser.datalevel = 8
            elif data == 'Started:':
                victrafficHTMLParser.datalevel = 10
            elif victrafficHTMLParser.datalevel == 10:
                victrafficHTMLParser.start = str.lstrip(data)
                victrafficHTMLParser.datalevel = 11
            elif data == 'Updated at:':
                victrafficHTMLParser.datalevel = 11
            elif victrafficHTMLParser.datalevel == 11:
                victrafficHTMLParser.updated = str.lstrip(data)
                victrafficHTMLParser.datalevel = 0
            elif victrafficHTMLParser.datalevel == 8:
                victrafficHTMLParser.info3 = str.lstrip(data)
                victrafficHTMLParser.datalevel = 9

            # Placing extracted data into dictionary
            info = {"Type": victrafficHTMLParser.mode,
                    "Location": victrafficHTMLParser.location,
                    "Area": victrafficHTMLParser.area,
                    "From": victrafficHTMLParser.lfrom,
                    "To": victrafficHTMLParser.lto,
                    "Near": victrafficHTMLParser.lnear,
                    "Info1": victrafficHTMLParser.info1,
                    "Info2": victrafficHTMLParser.info2,
                    "Info3": victrafficHTMLParser.info3,
                    "Started": victrafficHTMLParser.start,
                    "Updated": victrafficHTMLParser.updated}

            # Placing dictionary above into indexed dictionary
            dictofdicts[victrafficHTMLParser.index] = info

# Main Module
page = urllib.urlopen("http://traffic.vicroads.vic.gov.au/nojs/")
page = page.read()

parser = victrafficHTMLParser()

parser.feed(page)

print dictofdicts # temporarily used to view output
