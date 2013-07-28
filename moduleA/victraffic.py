# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with VicRoads-VicTraffic Website
################################################################################
import urllib

from HTMLParser import HTMLParser

# HTML Parser
class victrafficHTMLParser(HTMLParser):
    mode = 'DEFAULT' #initialise variables to be used later
    datalevel = 0
    location = ''
    locality = ''
    lfrom = ''
    lto = ''
    lnear = ''
    linfo1 = ''
    linfo2 = ''
    linfo3 = ''
    lstart = ''
    lupdated = ''
    index = 0
    dictofdicts = {}

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            #print "\n", str.upper(attrs[0][1]) #output for debug
            if str.upper(attrs[0][1]) == 'ALERT': #for data classification
                victrafficHTMLParser.mode = 'ALERT'
            elif str.upper(attrs[0][1]) == 'ROADWORKS':
                victrafficHTMLParser.mode = 'ROADWORKS'
            elif str.upper(attrs[0][1]) == 'EMERGENCY':
                victrafficHTMLParser.mode = 'EMERGENCY'
            else:
                victrafficHTMLParser.mode = 'DEFAULT'

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        if ("=" in data): #to remove nonsense data
            return
        elif str.strip(data): #to remove whitespace
            #print data #output for debug
            if victrafficHTMLParser.datalevel == 0:
                victrafficHTMLParser.location = '' #initialise for next round
                victrafficHTMLParser.locality = ''
                victrafficHTMLParser.lfrom = ''
                victrafficHTMLParser.lto = ''
                victrafficHTMLParser.lnear = ''
                victrafficHTMLParser.linfo1 = ''
                victrafficHTMLParser.linfo2 = ''
                victrafficHTMLParser.linfo3 = ''
                victrafficHTMLParser.lstart = ''
                victrafficHTMLParser.lupdated = ''
                victrafficHTMLParser.location = data
                victrafficHTMLParser.datalevel = 1
            elif data == 'From:':
                victrafficHTMLParser.datalevel = 3
            elif victrafficHTMLParser.datalevel == 3:
                victrafficHTMLParser.lfrom = data
                victrafficHTMLParser.datalevel = 4
            elif data == 'To:':
                victrafficHTMLParser.datalevel = 4
            elif victrafficHTMLParser.datalevel == 4:
                victrafficHTMLParser.lto = data
                victrafficHTMLParser.datalevel = 6
            elif data == 'Near:':
                victrafficHTMLParser.datalevel = 5
            elif victrafficHTMLParser.datalevel == 5:
                victrafficHTMLParser.lnear = data
                victrafficHTMLParser.datalevel = 6
            elif victrafficHTMLParser.datalevel == 1:
                victrafficHTMLParser.locality = data
                victrafficHTMLParser.datalevel = 2
            elif victrafficHTMLParser.datalevel == 6:
                victrafficHTMLParser.linfo1 = data
                victrafficHTMLParser.datalevel = 7
            elif victrafficHTMLParser.datalevel == 7:
                victrafficHTMLParser.linfo2 = data
                victrafficHTMLParser.datalevel = 8
            elif data == 'Started:':
                victrafficHTMLParser.datalevel = 10
            elif victrafficHTMLParser.datalevel == 10:
                victrafficHTMLParser.lstart = data
                victrafficHTMLParser.datalevel = 11
            elif data == 'Updated at:':
                victrafficHTMLParser.datalevel = 11
            elif victrafficHTMLParser.datalevel == 11:
                victrafficHTMLParser.lupdated = data
                victrafficHTMLParser.datalevel = 0
            elif victrafficHTMLParser.datalevel == 8:
                victrafficHTMLParser.linfo3 = data
                victrafficHTMLParser.datalevel = 9

            infod = {"Type": victrafficHTMLParser.mode, "Location": victrafficHTMLParser.location, "Locality": victrafficHTMLParser.locality, "From": victrafficHTMLParser.lfrom, "To": victrafficHTMLParser.lto, "Near": victrafficHTMLParser.lnear, "Info1": victrafficHTMLParser.linfo1, "Info2": victrafficHTMLParser.linfo2, "Info3": victrafficHTMLParser.linfo3, "Started": victrafficHTMLParser.lstart, "Updated": victrafficHTMLParser.lupdated}

            victrafficHTMLParser.dictofdicts.update(index=infod) #have not managed to append to dictionary yet

# Main Module
page = urllib.urlopen("http://traffic.vicroads.vic.gov.au/nojs/")
page = page.read()

parser = victrafficHTMLParser()

parser.feed(page)

print victrafficHTMLParser.dictofdicts
