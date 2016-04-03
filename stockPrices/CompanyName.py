import urllib2
from bs4 import BeautifulSoup

def getCompanyName(symbol, country):
	url = 'http://www.bloomberg.com/quote/' + symbol + ':' + country
	content = urllib2.urlopen(url).read()

	soup = BeautifulSoup(content, 'html.parser')

	return soup.find('h1', {'class': 'name'}).string.strip()

symbol = 'BABA'
country = 'US'

print(getCompanyName(symbol, country))