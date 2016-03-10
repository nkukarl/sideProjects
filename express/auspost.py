import urllib2
from bs4 import BeautifulSoup

trackingIDs = [63304477870067, 63304477869061, 63304477887065, 63304477862062]

for trackingID in trackingIDs[:1]:
	url = 'http://auspost.com.au/parcels-mail/track.html?ilink=fsr-tracking-track-your-item#/track?id=' + str(trackingID)

	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content, 'html.parser')

	print(soup)

	# print soup.find_all('div', {'class': 'statusHeader ng-binding ng-scope'})