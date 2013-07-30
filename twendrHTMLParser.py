# UoM Telstra M2M Challenge
#HTML Information Extractor
#twendr.com
# James Cocks
################################################################
import urllib

from HTMLParser import HTMLParser


#HTML Parser
class twendrHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
      return
    def handle_endtag(self, tag):
        return
    def handle_data(self, data):
        if ("=" in data): #pinched from someone else's. Makes it look better!
            return
        elif str.strip(data):
            ###############
            print data


# Main Module
page = urllib.urlopen("http://twendr.com/this_hour/across/23424748")
pageRead = page.read()

parser = twendrHTMLParser()

ParsedPageRead = parser.feed(pageRead)
print ParsedPageRead
