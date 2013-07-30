import urllib

from HTMLParser import HTMLParser

# function sort the order of data
def display(name,price):
    space={}
    for i in price.keys():
         #match the start ponit of prices
         if i%2 ==0:
            if len(price[i])>len(price[i+1]): 
               space[i+1]=''
               space[i]='\r'
            elif len(price[i])<len(price[i+1]):
                 space[i]=''
                 space[i+1]='\r'
            else:
                 space[i]='\r'
                 space[i+1]='\r'
    #forming a table of list
    print name[0],name[1],name[2],name[3],name[4]
    print price[0],space[0],price[2],space[2],price[4],space[4],price[6],space[6],price[8]
    print price[1],space[1],price[3],space[3],price[5],space[5],price[7],space[7],price[9],'\n\n'

#parser function
class ASXhtmlparser(HTMLParser):
      title=False
      name=False
      price=False
      
      ASX_name={}
      ASX_price={}
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
             ASXhtmlparser.price=True
          else:
             ASXhtmlparser.price=False
          return
      def handle_endtag(self,tag):
          return
             
      def handle_data(self,data):
          if ASXhtmlparser.title:
             print data
          if ASXhtmlparser.name and data != '\r\n'and data!='\n\n'and data!='\n ':
             ASXhtmlparser.ASX_name[ASXhtmlparser.n1]=data
             ASXhtmlparser.n1+=1
          if ASXhtmlparser.price and data != '\r\n'and data!='\n\n'and data!='\n ':
             ASXhtmlparser.ASX_price[ASXhtmlparser.n2]=data
             ASXhtmlparser.n2+=1
          return
#top 5 gain             
page1 = urllib.urlopen("http://www.asx.com.au/asx/widget/topDeclines.do")
page1=page1.read()
parser=ASXhtmlparser()
parser.feed(page1)
display(ASXhtmlparser.ASX_name,ASXhtmlparser.ASX_price)
#renew gloable varibles
ASXhtmlparser.ASX_name={}
ASXhtmlparser.ASX_price={}
ASXhtmlparser.n1=0
ASXhtmlparser.n2=0
ASXhtmlparser.title=False
ASXhtmlparser.name=False
ASXhtmlparser.price=False
#top 5 declines
page2 = urllib.urlopen("http://www.asx.com.au/asx/widget/topGains.do")
page2=page2.read()
parser=ASXhtmlparser()
parser.feed(page2)
display(ASXhtmlparser.ASX_name,ASXhtmlparser.ASX_price)

