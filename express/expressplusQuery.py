import urllib2
from bs4 import BeautifulSoup


def query(trackingID):
	base = 'http://www.expressplus.com.au/cgi-bin/GInfo.dll?EmmisTrack&w=expressplus&cno='
	url = base + str(trackingID)

	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content, 'html.parser')

	tables = soup.find_all('td', {'class' : ['trackListOdd', 'trackListEven']})

	# for row in tables:
	# 	print(row.string.encode('utf8'))

	status = tables[-3:]
	# for t in tables:
	# 	print t.text.encode('utf8')
	destination = soup.find(id = 'HeaderDes').text[7:].encode('utf8')

	print trackingID, destination

	for s in status:
		print s.string.encode('utf8')
	print '*' * 30

# trackingIDs = [14184926647, 14184926648, 14184926649, 14184926656, 14184926657, 14184926658, 14184926659, 14184926661, 14184926662, 14184933197]
trackingIDs = []

# for trackingID in trackingIDs:
# 	query(trackingID)

# Multithread
from threading import Thread
for trackingID in trackingIDs:
	t = Thread(target = query, args = (trackingID,))
	t.start()