import urllib2, re, easygui
from bs4 import BeautifulSoup

def main():
	msg = 'Please choose from the following:'
	title = 'Modify tracking IDs or Query'
	choices = ['Modify', 'Query']

	choice = easygui.buttonbox(msg, title, choices)

	if choice == choices[0]:
		modify()
	elif choice == choices[1]:
		queryFunc()


def modify():
	msg = 'Please choose from the following:'
	title = 'Modify tracking IDs or Query'
	choices = ['Add', 'Remove']

	choice = easygui.buttonbox(msg, title, choices)

	if choice == choices[0]:
		add()
	elif choice == choices[1]:
		remove()

def add():
	while True:
		msg = 'Please add an ID'
		title = 'Add ID(s)'
		trackingID = easygui.enterbox(msg, title)
		if not trackingID:
			break
		f = open('trackingIDs.txt', 'a')
		f.write(trackingID + '\n')
		f.close()

def remove():
	f = open('trackingIDs.txt')
	trackingIDs = f.read().split('\n')[:-1]
	f.close()
	msg = 'Please select an ID'
	title = 'Remove ID'
	trackingID = easygui.choicebox(msg, title, trackingIDs)

	trackingIDs.remove(trackingID)

	f = open('trackingIDs.txt', 'w+')
	for trackingID in trackingIDs:
		f.write(str(trackingID) + '\n')
	f.close()

def queryFunc():
	msg = 'Please choose from the following:'
	title = 'Query'
	queryTypes = ['Query One', 'Query All']

	queryType = easygui.buttonbox(msg, title, queryTypes)

	if queryType == queryTypes[0]:
		msg = 'Please enter an ID'
		title = 'Tracking ID'
		trackingID = easygui.enterbox(msg, title)
		info = queryOne(trackingID)
		queryResultDisplay(info)
	elif queryType == queryTypes[1]:
		queryAll()

def queryAll():
	f = open('trackingIDs.txt')
	trackingIDs = f.read().split('\n')[:-1]
	f.close()
	m = len(trackingIDs)

	f = open('result.txt', 'a')
	for i in range(m):
		info = queryOne(trackingIDs[i])
		f.write('\n'.join(info) + '\n\n')
	f.close()

	# easygui.msgbox('Query result saved in result.txt')

def queryOne(trackingID):
	base = 'http://www.expressplus.com.au/cgi-bin/GInfo.dll?EmmisTrack&w=expressplus&cno='
	trackingID = str(trackingID)
	url = base + trackingID

	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content, 'html.parser')

	tables = soup.find_all('td', {'class' : ['trackListOdd', 'trackListEven']})

	# for row in tables:
	# 	print(row.string.encode('utf8'))

	time, place, status = tables[-3:]
	destination = soup.find(id = 'HeaderDes').text[7:].strip().encode('utf8')

	time = time.string.strip().encode('utf8')
	place = place.string.strip().encode('utf8')
	status = status.string.strip().encode('utf8')

	# print trackingID, destination, '\n', time, place, status, '\n'
	return [trackingID, destination, time, place, status]
	
def queryResultDisplay(info):
	
	msg = '\n'.join(info)
	easygui.msgbox(msg)

# trackingIDs = [14184926647, 14184926648, 14184926649, 14184926656, 14184926657, 14184926658, 14184926659, 14184926661, 14184926662, 14184933197]

# f = open('trackingIDs.txt', 'w+')
# for trackingID in trackingIDs:
# 	f.write(str(trackingID) + '\n')
# f.close()

# trackingID = '14184926658'
# queryOne(trackingID)

main()

# f = open('trackingIDs.txt')
# trackingIDs = f.read().split('\n')[:-1]
# f.close()
# msg = 'Please select one or more IDs'
# title = 'Remove ID(s)'
# selectedIDs = easygui.multchoicebox(msg, title, trackingIDs)

# print(selectedIDs)