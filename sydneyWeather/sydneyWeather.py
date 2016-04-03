import urllib2, xlsxwriter, datetime

'''
This program acquires the daily weather observation of Sydney of the user specified year and month and write it to an excel workbook.
Meta data are saved in a separate text file.
Raw data are presented on Sheet1 and a wind rose showing the dominant wind direction is on Sheet2.

Library dependency: urllib2, xlsxwriter, datetime
'''

def getWeatherData(year, month):

	# customise year month
	yearMonth = '%04d' % year + '%02d' % month

	# url to csv file
	url = 'http://www.bom.gov.au/climate/dwo/' + yearMonth + '/text/IDCJDW2124.' + yearMonth + '.csv'

	# parse csv file to get raw data
	raw = urllib2.urlopen(url).read().split('\r\n')

	# separate meta data
	meta = '\n'.join(raw[:8])
	f = open('IDCJDW2124_' + yearMonth + '_meta.txt', 'w+')
	f.write(meta)
	f.close()

	# data of interest
	content = [row.split(',')[1:] for row in raw[10:]]

	# define number of rows and number of columns
	m, n = len(content), len(content[0])

	# create workbook
	wb = xlsxwriter.Workbook('IDCJDW2124_' + yearMonth + '.xlsx')
	# add Sheet1
	raw_sheet = wb.add_worksheet()

	# extract column headers
	headers = raw[9].split(',')[1:]

	# print(headers)

	# replace degree character
	col = 0
	for h in headers:
		raw_sheet.write(0, col, headers[col].replace('\xb0', 'degree ').replace('"', ''))
		col += 1

	# define date and time format
	date_format = wb.add_format({'num_format': 'd/mm/yyyy'})
	time_format = wb.add_format({'num_format': 'HH:MM'})

	# wind direction table
	directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
	# days array to record the number of days corresponding to each direction
	days = [0] * 16
	# initialise windSummary dictionary
	windSummary = dict()

	# write to Sheet1
	for row in range(1, m + 1):
		for col in range(n):
			# 1st column (col = 0) contains dates
			if col == 0:
				if content[row - 1][col]:
					date = datetime.datetime.strptime(content[row - 1][col], '%Y-%m-%d')
					raw_sheet.write(row, col, date, date_format)

			# 9th column (col = 9) contains time
			elif col == 8:
				if content[row - 1][col]:
					time = datetime.datetime.strptime(content[row - 1][col], '%H:%M')
					raw_sheet.write(row, col, time, time_format)
			# otherwise, column might contain number or text
			else:
				# try to convert content into float
				try:
					raw_sheet.write(row, col, float(content[row - 1][col]))
				# directly write text to Sheet1
				except:
					raw_sheet.write(row, col, content[row - 1][col])
			# special consideration for 7th column, record the number of days for each direction
			if col == 6:
				windDir = content[row - 1][col]
				windSummary[windDir] = windSummary.get(windDir, 0) + 1

	
	# update days array, align days with correct order of directions
	for i in range(16):
		d = directions[i]
		days[i] = windSummary.get(d, 0)


	# add Sheet2 for the wind data
	wind_sheet = wb.add_worksheet()
	# add headers
	wind_sheet.write(0, 0, 'Direction')
	wind_sheet.write(0, 1, 'Days')
	# add wind data
	wind_sheet.write_column(1, 0, directions)
	wind_sheet.write_column(1, 1, days)

	# add chart
	chart = wb.add_chart({'type': 'radar'})
	# add series
	chart.add_series({
		'name': '=Sheet2!$B$1',
		'categories': '=Sheet2!$A$2:$A$17',
		'values': '=Sheet2!$B$2:$B$17',
	})
	# add title
	chart.set_title({'name': 'Wind rose'})
	# place chart
	wind_sheet.insert_chart('D3', chart)
	wb.close()

if __name__ == '__main__':
	getWeatherData(2016, 3)