import urllib2
from bs4 import BeautifulSoup


def query(trackingID):
	base = 'http://declare.30post.cn/admin888/statusManager/search.asp?a=search&expressno='
	url = base + str(trackingID)

	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content, 'html.parser', from_encoding = 'GB18030')

	status = soup.find_all('ul', {'class': 'Status'})[0]
	info = status.find_all('li')
	for i in info:
		if i:
			print i.text.encode('utf8').strip()

	statusTime = soup.find_all('span', {'class': 'statusTime'})[0].string.encode('utf8').strip()
	statusText = soup.find_all('span', {'class': 'statusText'})[0].string.encode('utf8').strip()

	# print trackingID
	print statusTime
	print statusText

trackingIDs = ['K8000194846E', 'K8000194848E']

# for trackingID in trackingIDs:
# 	query(trackingID)

# Multithread
from threading import Thread
for trackingID in trackingIDs:
	t = Thread(target = query, args = (trackingID,))
	t.start()