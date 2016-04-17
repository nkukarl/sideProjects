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

	print trackingID,
	# if LEFT and RIGHT:
	# 	if LEFT[-1].find('span').string:
	# 		status = LEFT[-1].find('span').string.encode('utf8')
	# 		print status,
	# 	if RIGHT[-1].find('span').string:
	# 		lastUpdate = RIGHT[-1].find('span').string.encode('utf8')
	# 	print lastUpdate
	# else:
	# 	print 'NOT FOUND'

	print soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lbTTLCurrentStatus'}).text.encode('utf8')

# trackingIDs = [770001634144, 770001634143, 660003228335, 660003228567, 660003228297, 660003228507]
trackingIDs = [770001634290, 770001634292, 770001634407, 770001634409, 770001634410, 770001634411]

# for trackingID in trackingIDs:
# 	query(trackingID)

from threading import Thread

for trackingID in trackingIDs:
	t = Thread(target = query, args = (trackingID,))
	t.start()