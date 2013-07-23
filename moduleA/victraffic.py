# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with VicRoads-VicTraffic Website
################################################################################
import urllib

from HTMLParser import HTMLParser

# HTML Parser
class victrafficHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "li":
            print "\n", str.upper(attrs[0][1])

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        if ("=" in data):
            return
        elif str.strip(data):
            print data
      
# Main Module
page = urllib.urlopen("http://traffic.vicroads.vic.gov.au/nojs/")
page = page.read()

parser = victrafficHTMLParser()

parser.feed(page)
