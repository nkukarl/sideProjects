import urllib2
from bs4 import BeautifulSoup
from tabulate import tabulate

'''
get stock price ladder for Chinese stock using sina database
'''
def getPriceLadder(stocks):

	# source: sina realtime stock price
	base = 'http://hq.sinajs.cn/list='
	query = ','.join(stocks)
	url = base + query

	content = urllib2.urlopen(url).read()
	# create beautifulsoup object (original encoding GB18030)
	soup = BeautifulSoup(content, 'html.parser', from_encoding = 'GB18030')

	# get string from soup
	string = soup.string

	lst = string.split('\n')[:-1]

	# raw: raw data for each stock/index in lst
	for raw in lst:
		# symbol -> stock symbol
		symbol = raw[11:19].upper()
		# stock info (splitted by ',')
		info = raw[21:-2].split(',')
		# company name from info (encode using 'utf8')
		name = info.pop(0).encode('utf8')

		# initialise summary dictionary and define keys
		summary = dict()
		keys = ['todayOpen', 'lastClose', 'cur', 'todayHigh', 'todayLow', 'bid', 'ask', 'volume', 'total transaction']

		# get values from info using keys
		for k in keys:
			summary[k] = info.pop(0)

		# show price difference and price difference in percentage by comparing current price with lastClose price
		diff = float(summary['cur']) - float(summary['lastClose'])
		diffPct = float(diff) / float(summary['lastClose']) * 100

		# create price ladder
		ladder = []
		for i in range(5): # get bid info (volume and price)
			v, p = info.pop(0), info.pop(0)
			ladder.append([v, p, '', ''])
		
		for i in range(5): # get ask info (volume and price)
			v, p = info.pop(0), info.pop(0)
			ladder.insert(0, ['', '', p, v])

		# get date and time info
		date = info.pop(0)
		time = info.pop(0)

		# formulate display content
		print date, time

		# print stock name, symbol, currency symbol and price, price change and price change in percentage
		print name, '(' + symbol + ')', (u'\u00A5' + summary['cur']).encode('utf8'), diff, str(round(diffPct, 2)) + '%'

		# print previous close info
		print 'Previous Close', summary['lastClose']

		# print today's open, high and low using tables created by tabulate library
		header = ['Open', 'High', 'Low']
		todayPerformance = [[summary['todayOpen'], summary['todayHigh'], summary['todayLow']]]
		print tabulate(todayPerformance, headers = header, tablefmt = 'grid')

		# display bid and ask info when symbol is not index
		if symbol != 'SH000001' and symbol != 'SZ399001':

			header = ['Bid Volume', 'Bid Price', 'Ask Price', 'Ask Volume']
			print tabulate(ladder, headers = header, tablefmt = 'grid')

		print

if __name__ == '__main__':

	indices = 'sh000001', 'sz399001'
	getPriceLadder(indices)

	stocks = ['sh601328', 'sh601166', 'sh601857', 'sh601318', 'sz300104', 'sz300274']
	getPriceLadder(stocks)