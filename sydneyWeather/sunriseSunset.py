import requests, xlsxwriter
from bs4 import BeautifulSoup

'''
This program acquires the sunrise and sunset time of Sydney throughout the entire year of 2016 using the sunrise and sunset computation program by Geoscience Australia.
Cleaning the raw data from Internet, writing rise and set times to a text file and an excel workbook.
Extract rise hour, rise minute, set hour, set minute, construct sunrise time, sunset time and compute day length from the difference between sunrise time and sunset time
Generate scatter plot to show sunrise/sunset time and day length
	- Show day length on secondary y axis
	- chart title
	- axis title
	- legend
'''

# form to be submitted
form = 'END=END&loc=yes&loc=no&lathemi=north&lathemi=south&longhemi=west&longhemi=east&Location=SYDNEY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++&LatDeg=-33&LatMin=52&LatSec=0&LongDeg=151&LongMin=12&LongSec=0&State=NSW+-+Sydney+%28most+location%29&DST=Yes&TZ=10&UTCOFF=11&ATZ=%28EDT%29&LT=11%3A46%3A01+AM&TimeZoneName=+&austzone=%2B10&TimeZone=%2B10&Event=7&Event=1&ZenithDeg=&ZenithMin=&ZenithSec=0&height=0&END=END&Date=2016&END=END'

# url to Geoscience Australia website
url = 'http://www.ga.gov.au/bin/geodesy/run/sunrisenset'

# acquire content from website
content = requests.post(url, data = form).text

# create BeautifulSoup object
soup = BeautifulSoup(content, 'html.parser')

# raw data in pre tag
rawData = soup.find('pre').string.encode('utf8')

# ignore metadata at the top
rawData = rawData.split('\n')[5:]

# format conversion of raw data, putting sunrise and sunset times in two columns in the order of time

'''
rise set
XXXX XXXX # Jan 1
XXXX XXXX # Jan 2
......
XXXX XXXX # Dec 30
XXXX XXXX # Dec 31
'''

tmpData = []

for row in rawData:
	if row:
		tmpData.append(row.replace('                 ', '    XXXX XXXX    ').replace('    ', '  ').split('  ')[1:])

# raw data are presented in two halves, Jan - Jun and Jul to Dec
# use firstHalf and secondHalf to store
# data from Jan to Jun
firstHalf = tmpData[2:33]
# data from Jul to Dec
secondHalf = tmpData[35:66]

# get data from firstHalf, add to tmpData
tmpData = [[] for _ in range(12)]
for row in firstHalf:
	for colIdx in range(6):
		if row[colIdx] != 'XXXX XXXX' and row[colIdx] != '':
			tmpData[colIdx].append(row[colIdx])

# get data from secondHalf, add to tmpData
for row in secondHalf:
	for colIdx in range(6):
		if row[colIdx] != 'XXXX XXXX' and row[colIdx] != '':
			tmpData[colIdx + 6].append(row[colIdx])

# generate processed data containing sunrise and sunset times
# XXXX XXXX
processed = []
for row in tmpData:
	processed += row

'''
Saving processed data to a text file (optional)
'''

'''
f = open('sunriseSunset.txt', 'w+')
f.write('\n'.join(processed))
f.close()
'''

# initialise sunriseRaws and sunsetRaws arrays to collect raw rise and set data
sunriseRaws, sunsetRaws = [], []

# create workbook
wb = xlsxwriter.Workbook('sunriseSunset.xlsx')
# create sheet
sheet = wb.add_worksheet()

# write column headers
sheet.write(0, 0, 'Date')
sheet.write(0, 1, 'rise')
sheet.write(0, 2, 'set')
sheet.write(0, 3, 'rise hour')
sheet.write(0, 4, 'rise minute')
sheet.write(0, 5, 'set hour')
sheet.write(0, 6, 'set minute')
sheet.write(0, 7, 'Sunrise Time')
sheet.write(0, 8, 'Sunset Time')
sheet.write(0, 9, 'Day Length')

# row number
row = 1

# integer corresponding to 01/01/2016
day = 42370

# date and time format
day_format = wb.add_format({'num_format': 'dd/mm/yy'})
time12_format = wb.add_format({'num_format': 'HH:MM AM/PM'})
time24_format = wb.add_format({'num_format': 'HH:MM'})

# iterate each processed array

for entry in processed:
	sunriseRaw, sunsetRaw = entry.split()
	sunriseRaws.append(sunriseRaw)
	sunsetRaws.append(sunsetRaw)
	
	# write date
	sheet.write('A' + str(row + 1), day, day_format);

	# extract hour and minute from column B, C and write to column D, E, F, G
	# extract
	sheet.write_formula(row, 3, 'left(B' + str(row + 1) + ', 2)')
	sheet.write_formula(row, 4, 'right(B' + str(row + 1) + ', 2)')
	sheet.write_formula(row, 5, 'left(C' + str(row + 1) + ', 2)')
	sheet.write_formula(row, 6, 'right(C' + str(row + 1) + ', 2)')
	# write
	sheet.write_formula(row, 7, 'time(D' + str(row + 1) + ', E' + str(row + 1) + ', 0)', time12_format)
	sheet.write_formula(row, 8, 'time(F' + str(row + 1) + ', G' + str(row + 1) + ', 0)', time12_format)
	sheet.write_formula(row, 9, 'I' + str(row + 1) + ' - H' + str(row + 1), time24_format)
	
	row += 1
	day += 1

# write sunriseRaws and sunsetRaws from column B, C
sheet.write_column(1, 1, sunriseRaws)
sheet.write_column(1, 2, sunsetRaws)

# add scatter - smooth chart

chart = wb.add_chart({'type': 'scatter', 'subtype': 'smooth'})

# add sunrise time
chart.add_series({
	'name': '=Sheet1!$H$1',
	'categories': '=Sheet1!$A$2:$A$' + str(len(sunriseRaws) + 1),
	'values': '=Sheet1!$H$2:$H$' + str(len(sunriseRaws) + 1),
	})

# add sunset time
chart.add_series({
	'name': '=Sheet1!$I$1',
	'categories': '=Sheet1!$A$2:$A$' + str(len(sunriseRaws) + 1),
	'values': '=Sheet1!$I$2:$I$' + str(len(sunriseRaws) + 1),
	})

# add day length
chart.add_series({
	'name': '=Sheet1!$J$1',
	'categories': '=Sheet1!$A$2:$A$' + str(len(sunriseRaws) + 1),
	'values': '=Sheet1!$J$2:$J$' + str(len(sunriseRaws) + 1),
	'y2_axis': 1,
	})

# set title, axis, legend
chart.set_title({'name': 'Sunrise Time, Sunset Time & Day Length'})
chart.set_x_axis({'name': 'Date', 'min': 42370, 'max': 42735})
chart.set_y_axis({'name': 'Sunrise/Sunset Time'})
chart.set_y2_axis({'name': 'Day Length', 'min': 0.35, 'max': 0.65})
chart.set_legend({'position': 'bottom'})

# set chart size
chart.set_size({'x_scale': 1.5, 'y_scale': 1.5 })

# insert chart to a certain position
sheet.insert_chart('C10', chart)

# close workbook
wb.close()