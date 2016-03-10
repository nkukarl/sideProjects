import urllib2, xlsxwriter, datetime
from bs4 import BeautifulSoup

def getWeatherData(year, month):

	yearMonth = '%04d' % year + '%02d' % month

	url = 'http://www.bom.gov.au/climate/dwo/' + yearMonth + '/text/IDCJDW2124.' + yearMonth + '.csv'

	raw = urllib2.urlopen(url).read().split('\r\n')

	meta = '\n'.join(raw[:8])
	f = open('IDCJDW2124_' + yearMonth + '_meta.txt', 'w+')
	f.write(meta)
	f.close()

	content = [row.split(',')[1:] for row in raw[10:]]

	m, n = len(content), len(content[0])

	wb = xlsxwriter.Workbook('IDCJDW2124_' + yearMonth + '.xlsx')
	sheet = wb.add_worksheet()

	headers = raw[9].split(',')[1:]

	# print(headers)

	col = 0
	for h in headers:
		sheet.write(0, col, headers[col].replace('\xb0', 'degree ').replace('"', ''))
		col += 1

	date_format = wb.add_format({'num_format': 'd/mm/yyyy'})
	time_format = wb.add_format({'num_format': 'HH:MM'})

	for row in range(1, m + 1):
		for col in range(n):
			if col == 0:
				if content[row - 1][col]:
					date = datetime.datetime.strptime(content[row - 1][col], '%Y-%m-%d')
					sheet.write(row, col, date, date_format)
			elif col == 8:
				if content[row - 1][col]:
					time = datetime.datetime.strptime(content[row - 1][col], '%H:%M')
					sheet.write(row, col, time, time_format)
			else:
				try:
					sheet.write(row, col, float(content[row - 1][col]))
				except:
					sheet.write(row, col, content[row - 1][col])

	wb.close()

# getWeatherData(2015, 5)