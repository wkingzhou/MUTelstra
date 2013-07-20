# UoM Telstra M2M Challenge
# HMTL Information Extractor
# for use with PTV Website
################################################################################
import urllib
import util.custom1
import time

# Main Module
page = urllib.urlopen("http://ptv.vic.gov.au/disruptions/")
page = page.readlines()

for line in page:
  if "a title" in line and "href" in line:
    print line
