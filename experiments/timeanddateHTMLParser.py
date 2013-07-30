# UoM Telstra M2M Challenge
#HTML Information Extractor
#THIS IS ONLY A TEST.
#Also, I'm not sure if we're allowed to use this one anyway,
#due to the site's source code which says
#   "scripts and programs that download content transparent to the user
#   are not allowed without permission"
# James Cocks
################################################################
import urllib

from HTMLParser import HTMLParser


#HTML Parser
class timeanddateHTMLParser(HTMLParser):
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
page = urllib.urlopen("http://www.timeanddate.com/worldclock/custom.html?continent=australasia")
pageRead = page.read()

parser = timeanddateHTMLParser()

ParsedPageRead = parser.feed(pageRead)
print ParsedPageRead
