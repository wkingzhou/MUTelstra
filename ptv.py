# UoM M2M Telstra Challenge
# HTML Information Extractor
# for use with http://ptv.vic.gov.au/disruptions/
# Renlord Y.
###############################################################################
# Libraries
import urllib

# key variables
site = "http://ptv.vic.gov.au/disruptions/"
wanted = []
# Useful Functions

# Main Module
page = urllib.urlopen(site)
page = page.readlines()

for line in page:
  if "<a title" in line:
    print line
