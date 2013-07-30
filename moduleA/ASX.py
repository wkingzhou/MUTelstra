import urllib

from HTMLParser import HTMLParser

# function sort the order of data
def display(name,price1,price2):
    space1={}
    space2={}
    for i in price1.keys():
         #match the start ponit of prices
        if len(price1[i])>len(price2[i]): 
               space2[i]='  '
               space1[i]=' '
        elif len(price1[i])<len(price2[i]):
                 space1[i]='  '
                 space2[i]=' '
        else:
                 space1[i]=' '
                 space2[i]=' '
    #forming a table of list (only up to 5 now)
    print name[0],name[1],name[2],name[3],name[4]
    print ''.join(map(str,[price1[0],space1[0],price1[1],space1[1],price1[2],space1[2],price1[3],space1[3],price1[4]]))
    print ''.join(map(str,[price2[0],space2[0],price2[1],space2[1],price2[2],space2[2],price2[3],space2[3],price2[4]]))
    print '\n\n\n'
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
#top 5 declines
page1 = urllib.urlopen("http://www.asx.com.au/asx/widget/topDeclines.do")
page1=page1.read()
parser=ASXhtmlparser()
parser.feed(page1)
print 'Top 5 Declines'
nameD5=ASXhtmlparser.ASX_name #top 5 decline name
priceD5=ASXhtmlparser.ASX_price1 #top 5 ecline price
changeD5=ASXhtmlparser.ASX_price2 #top 5 decline changed vaule
display(nameD5,priceD5,changeD5)
#renew gloable varibles
ASXhtmlparser.ASX_name={}
ASXhtmlparser.ASX_price1={}
ASXhtmlparser.ASX_price2={}
ASXhtmlparser.n0=0
ASXhtmlparser.n1=0
ASXhtmlparser.n2=0
ASXhtmlparser.title=False
ASXhtmlparser.name=False
ASXhtmlparser.price0=False
ASXhtmlparser.price1=True
ASXhtmlparser.price2=False
#top 5 gain
page2 = urllib.urlopen("http://www.asx.com.au/asx/widget/topGains.do")
page2=page2.read()
parser=ASXhtmlparser()
parser.feed(page2)
print 'Top 5 Gain'
nameG5=ASXhtmlparser.ASX_name #top 5 Gain name
priceG5=ASXhtmlparser.ASX_price1 #top 5 Gain price
changeG5=ASXhtmlparser.ASX_price2 #top 5 Gain changed vaule
display(nameG5,priceG5,changeG5)


#renew gloable varibles
ASXhtmlparser.ASX_name={}
ASXhtmlparser.ASX_price1={}
ASXhtmlparser.ASX_price2={}
ASXhtmlparser.n0=0
ASXhtmlparser.n1=0
ASXhtmlparser.n2=0
ASXhtmlparser.title=False
ASXhtmlparser.name=False
ASXhtmlparser.price0=False
ASXhtmlparser.price1=True
ASXhtmlparser.price2=False
#top 50 total
page2 = urllib.urlopen("http://www.asx.com.au/asx/widget/topCompanies.do")
page2=page2.read()
parser=ASXhtmlparser()
parser.feed(page2)
#hasn't arrange top 50 ones
name50=ASXhtmlparser.ASX_name #top 5 Gain name
price50=ASXhtmlparser.ASX_price1 #top 5 Gain price
change50=ASXhtmlparser.ASX_price2 #top 5 Gain changed vaule
print name50
print price50
print change50


