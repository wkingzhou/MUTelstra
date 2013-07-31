import urllib

from HTMLParser import HTMLParser


#parser function
class ASXhtmlparser(HTMLParser):
      title=False
      name=False
      price0=False #price0 indicate if data is a price;
      price1=True  #price1 indicate if it's a price;
      price2=False #price2 indicate if it's a change in price
      ASX_name={}  #title str
      ASX_price1={}#'price' str in array
      ASX_price2={}#'change of price' str in array
      n0=0
      n1=0
      n2=0
      def handle_starttag(self,tag,attrs):
          if tag == 'title':
             ASXhtmlparser.title=True
          else:
             ASXhtmlparser.title=False 
          if tag == 'td' and attrs ==[('class','code')]:
             ASXhtmlparser.name=True
          else:
             ASXhtmlparser.name=False
          if tag == 'td' and attrs ==[('class','right')]:
             ASXhtmlparser.price0=True
          else:
             ASXhtmlparser.price0=False
          return
      def handle_endtag(self,tag):
          return
             
      def handle_data(self,data):
          if ASXhtmlparser.title:
             print data
          if ASXhtmlparser.name and data[0] != '\r'and data[0]!='\n'and data[0]!='\t':
             ASXhtmlparser.ASX_name[ASXhtmlparser.n0]=data
             ASXhtmlparser.n0+=1
          if ASXhtmlparser.price0 and ASXhtmlparser.price1 and data[0] != '\r'and data[0]!='\n'and data[0]!='\t' :
             ASXhtmlparser.ASX_price1[ASXhtmlparser.n1]=data
             ASXhtmlparser.n1+=1
             ASXhtmlparser.price1=False
             ASXhtmlparser.price2=True
          elif ASXhtmlparser.price0 and ASXhtmlparser.price2 and data[0] != '\r'and data[0]!='\n'and data[0]!='\t':
               ASXhtmlparser.ASX_price2[ASXhtmlparser.n2]=data
               ASXhtmlparser.n2+=1
               ASXhtmlparser.price1=True
               ASXhtmlparser.price2=False
              
          return

#top 50 total
page2 = urllib.urlopen("http://www.asx.com.au/asx/widget/topCompanies.do")
page2=page2.read()
parser=ASXhtmlparser()
parser.feed(page2)
ASXdict={} #inital ASX dictonary (20min delay for each refreash from web)
for i in ASXhtmlparser.ASX_name.keys():
    info={"name":ASXhtmlparser.ASX_name[i],  #name indicate name of the company
         "price":ASXhtmlparser.ASX_price1[i], #price shows the current share price
         "detprice":ASXhtmlparser.ASX_price2[i]} #detprice shows change in share price 
    ASXdict[i] = info
print ASXdict
