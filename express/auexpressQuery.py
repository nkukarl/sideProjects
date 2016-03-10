import urllib2
from bs4 import BeautifulSoup



def query(trackingID):
	trackingID = str(trackingID)

	form = 'OrderId=' + str(trackingID)
	url = 'http://www.auexpress.com.au/TOrderQuery_Service.aspx'

	req = urllib2.Request(url, form)
	content = urllib2.urlopen(req).read()

	soup = BeautifulSoup(content, 'html.parser')

	LEFT = soup.find_all('td', {'class': 'Col_Left'})
	RIGHT = soup.find_all('td', {'class': 'Col_Right'})

	if LEFT and RIGHT:
		status = LEFT[-1].find('span').string.encode('utf8')
		lastUpdate = RIGHT[-1].find('span').string.encode('utf8')
		print trackingID, status, lastUpdate
	else:
		print trackingID, 'NOT FOUND'

# trackingIDs = [770001634144, 770001634143, 660003228335, 660003228567, 660003228297, 660003228507]
trackingIDs = [770001634290, 770001634292]

# for trackingID in trackingIDs:
# 	query(trackingID)

from threading import Thread

for trackingID in trackingIDs:
	t = Thread(target = query, args = (trackingID,))
	t.start()