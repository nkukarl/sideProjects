import requests, xlsxwriter
from bs4 import BeautifulSoup

form = 'END=END&loc=yes&loc=no&lathemi=north&lathemi=south&longhemi=west&longhemi=east&Location=SYDNEY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++&LatDeg=-33&LatMin=52&LatSec=0&LongDeg=151&LongMin=12&LongSec=0&State=NSW+-+Sydney+%28most+location%29&DST=Yes&TZ=10&UTCOFF=11&ATZ=%28EDT%29&LT=11%3A46%3A01+AM&TimeZoneName=+&austzone=%2B10.5&TimeZone=%2B10.5&Event=7&Event=1&ZenithDeg=&ZenithMin=&ZenithSec=0&height=0&END=END&Date=2016&END=END'
url = 'http://www.ga.gov.au/bin/geodesy/run/sunrisenset'

content = requests.post(url, data = form).text

soup = BeautifulSoup(content, 'html.parser')

rawData = soup.find('pre').string.encode('utf8')

rawData = rawData.split('\n')[5:]

tmpData = []

for row in rawData:
	if row:
		tmpData.append(row.replace('                 ', '    XXXX XXXX    ').replace('    ', '  ').split('  ')[1:])

firstHalf = tmpData[2:33]
secondHalf = tmpData[35:66]

tmpData = [[] for _ in range(12)]
for row in firstHalf:
	for colIdx in range(6):
		if row[colIdx] != 'XXXX XXXX' and row[colIdx] != '':
			tmpData[colIdx].append(row[colIdx])

for row in secondHalf:
	for colIdx in range(6):
		if row[colIdx] != 'XXXX XXXX' and row[colIdx] != '':
			tmpData[colIdx + 6].append(row[colIdx])

processed = []
for row in tmpData:
	processed += row

# # f = open('sunriseSunset.txt', 'w+')
# # f.write('\n'.join(processed))
# # f.close()

# f = open('sunriseSunset.txt')
# processed = f.read().split('\n')

sunriseRaws, sunsetRaws = [], []
sunriseHours, sunriseMinutes = [], []
sunsetHours, sunsetMinutes = [], []

for entry in processed:
	sunriseRaw, sunsetRaw = entry.split()
	sunriseRaws.append(sunriseRaw)
	sunsetRaws.append(sunsetRaw)
	
	# sunriseHour, sunriseMinute = sunriseRaw[:2], sunriseRaw[2:]
	# sunsetHour, sunsetMinute = sunsetRaw[:2], sunsetRaw[2:]
	# sunriseHours.append(int(sunriseHour))
	# sunriseMinutes.append(int(sunriseMinute))
	# sunsetHours.append(int(sunsetHour))
	# sunsetMinutes.append(int(sunsetMinute))


wb = xlsxwriter.Workbook('sunriseSunset.xlsx')
sheet = wb.add_worksheet()
sheet.write(0, 0, 'rise')
sheet.write(0, 1, 'set')
sheet.write_column(1, 0, sunriseRaws)
sheet.write_column(1, 1, sunsetRaws)

# sheet.write(0, 2, 'rise hour')
# sheet.write(0, 3, 'rise minute')
# sheet.write(0, 4, 'set hour')
# sheet.write(0, 5, 'set minute')
# sheet.write_column(1, 2, sunriseHours)
# sheet.write_column(1, 3, sunriseMinutes)
# sheet.write_column(1, 4, sunsetHours)
# sheet.write_column(1, 5, sunsetMinutes)

wb.close()