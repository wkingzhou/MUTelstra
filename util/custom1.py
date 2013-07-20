# UoM M2M Telstra Challenge
# Python Utility
# HTML Handling

from HTMLParser import HTMLParser

class TestHMTLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "start tag:", tag
    def handle_endtag(self, tag):
        print 
    def handle_data(self, data):

def htmltag_stripper(string):
    while("<" in string or ">" in string):
        start = string.index("<")
        end = string.index(">")
        if(start < end):
            if(start != 0):
                new_string = string[:start]
                break
            else:
                string = string[end+1:]
        else:
            string = string[1:]
    return new_string

"""
Use this function to retain the list of tags as listed in tag_list
PARAM:
    @tag_list, list of tags that you want to retain.
    @text, (LIST) HTML document to filter.
RETURNS
    string containing the tags and information you wished to retain.
"""
def retain(tag_list, text):

                      
