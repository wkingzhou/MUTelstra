# -*- coding: utf-8 -*- 
#
# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with Guardian Website (mobile version)
# James Cocks, using a template by Renlord Y.
# Note there are still some bugs when the parser encounters unicode, but
# I think I'll post it up here for others to look at - I've been struggling to
# fix it for a fair while unsuccessfully.
################################################################################
import urllib
import time

from HTMLParser import HTMLParser

# Custom Omissions
blocked_urls = ["uk-news/", "world/", "commentisfree/", "sport/", \
                "football/", "lifeandstyle/", "culture/", "business/", \
                "travel/", "technology/", "environment/", "top-stories/"]
          
parserToggle = False
          
#Blocked data
BlockedData = ['About this site',  'Help', 'Contact us', 'Feedback',\
               'Terms ', '&', ' conditions','Privacy policy','Cookie policy']
unwantedTitleChars = '&nbsp;'#don't want this in the News titles


# HTML Parser
class GuardianHTMLParser(HTMLParser):
   ####### news = {'Name' : '', 'Picture' : ''}
    attrsType = ''
    #toggle_mode = 0
    parserToggle = False
    showNextImage = False   #toggles when a relevant headline pops up.
                            #Means that we can get the urls for only the
                            #pictures relevant to the news titles.
    toggle_mode = 'DEFAULT'

    imageThenText = False   # = True when the source contains the image, followed by the text.
                            # = False otherwise.
    h2_text = False
    
    sameData = False    #prevents data to be mistaken for multiple different
                        #entries.
    lastData = ''       #Keeps a record of what the last data entry was for
                        #the title text, so that it can be concatenated.
    
    def handle_starttag(self, tag, attrs):
#        print 'START TAG::::::: ' + tag
        GuardianHTMLParser.sameData = False
        GuardianHTMLParser.lastData = ''
        blocking = False

        GuardianHTMLParser.parserToggle = False
        if tag == "a" and attrs[0][0] == 'href':
            if attrs[1][0] == 'class':
                if attrs[1][1] == 'link-text':
                    GuardianHTMLParser.attrsType = 'link-text'
                    GuardianHTMLParser.parserToggle = True
                    for url in blocked_urls:
                        if url == attrs[1][1]:
                            blocking = True
                            GuardianHTMLParser.parserToggle = False
                            break
                elif attrs[1][1] == "media__img trail__img":
                    GuardianHTMLParser.attrsType = 'image'
                    GuardianHTMLParser.showNextImage = True
                    GuardianHTMLParser.parserToggle = True
                    #return
           
            elif str(attrs[1][1])[-4:] == 'text':#For titles, the last 4 chars of
                GuardianHTMLParser.parserToggle = True #the second subelement of the
                GuardianHTMLParser.attrsType = 'link-text'#second element is 'text'        

        if tag == "img":
            #print attrs
            if (attrs[0][1] == 'maxed' or \
            attrs[1][0] == "data-lowsrc"):# and GuardianHTMLParser.parserToggle == True:
                print 'PICTURE URL: ' + attrs[1][1]#print out the url of the image.
                GuardianHTMLParser.attrsType = 'image'
                GuardianHTMLParser.showNextImage = True
                GuardianHTMLParser.parserToggle = True
                #return
        
        elif tag == "div":
            if attrs == [('class', 'trail__text')]:
                if attrs[0][1] == 'trail__text':
                    GuardianHTMLParser.parserToggle = True
                    GuardianHTMLParser.showNextImage = True
                    GuardianHTMLParser.attrsType = 'trail-text'
                    #return

        elif tag == 'h2':
            GuardianHTMLParser.h2_text = True
            GuardianHTMLParser.parserToggle = True
                
                
    #        else:
   #           print attrs
            if not blocking:
                return
        return

    def handle_endtag(self, tag):

        if tag == 'h2':
            GuardianHTMLParser.h2_text = False
        elif tag == 'img':
            GuardianHTMLParser.showNextImage = False


        if GuardianHTMLParser.sameData == True:
            print GuardianHTMLParser.lastData
        GuardianHTMLParser.sameData = False
        GuardianHTMLParser.lastData = ''
        return

    def handle_data(self, data):
        
        if str.strip(data):
            if GuardianHTMLParser.parserToggle == True:
                if GuardianHTMLParser.attrsType == 'link-text' or \
                   GuardianHTMLParser.attrsType == 'trail-text' or \
                   GuardianHTMLParser.attrsType == 'image':
                        
                    if data not in BlockedData:
                        if GuardianHTMLParser.attrsType == 'link-text':
                            if unwantedTitleChars in data:
                                data = data.replace(unwantedTitleChars, ' ')

                            if GuardianHTMLParser.sameData == True:
                                data = GuardianHTMLParser.lastData + data
                            else:
                                print 'TITLE: ' + data.strip(' \t\n\r').upper()
                        else:
                            print 'SubTitle: ' + data.strip(' ')

       #             if GuardianHTMLParser.attrsType == 'image':#This doesn't seem to work...
       #                 print 'PICTURE URL: ' + data.strip(' ')                       
               
                else:
                    print 'wat'
            
        
        GuardianHTMLParser.lastData = data   #in case there's any stuffups with the
                                        #page's layout
        return

# Main Module
page = urllib.urlopen("http://m.guardian.co.uk/australia")
page = page.read()

parser = GuardianHTMLParser()

toggle_data = False

parser.feed(page)
