import json, urllib2, pytz, datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# acquire latest daily stock price variation using bloomberg website

def dailyPrice(symbol, country, companyName):
	'''
	get daily stock price variation and save it to a pdf file
	'''

	# get data from bloomberg market chart data
	url = 'http://www.bloomberg.com/markets/chart/data/1D/' + symbol + ':' + country
	response = urllib2.urlopen(url)
	# create json object
	data = json.load(response)

	# acquire 'data_values' attribute of json object
	# datapoints -> [[t1, p1], [t2, p2], [t3, p3], ..., [tn, pn]]
	# tX is in epoch time format, pX is stock price corresponding to tX
	datapoints = data['data_values']

	# extract epoch time and prices from datapoints
	epochTimes = []
	prices = []

	for dp in datapoints:
		rawTime, price = dp
		epochTimes.append(rawTime // 1000)
		prices.append(price)

	# creating three time zones for US, Australia and China
	est = pytz.timezone('US/Eastern')
	aest = pytz.timezone('Australia/Sydney')
	ctz = pytz.timezone('Asia/Urumqi')

	# creating time zone and local currency map
	tzMAP = {'US': est, 'AU': aest, 'CH': ctz}
	currencyMAP = {'US': 'USD', 'AU': 'AUD', 'CH': 'CNY'}

	# data provided by bloomberg using US time, original timezone is est
	tzOrg = est
	# destination time zone is determined using stock's country code
	tzFin = tzMAP[country]

	# get final time for correct time zone
	final_time = epochTimeConversion(epochTimes, tzOrg, tzFin)

	# acquire trading date from final time
	tradingDate = str(final_time[0])[:10]

	# generate plot showing stock price variation
	fig = plt.figure()
	plt.plot(final_time, prices, label = symbol + ':' + country)
	plt.xlabel('Time', size = 15)
	plt.ylabel('Stock price ' + '(' + currencyMAP[country] + ')', size = 15)
	plt.legend(loc = 1)
	# use company name and trading date as plot title
	plt.title(companyName + ' (' + tradingDate + ')', size = 15) 
	# set y axis lower and upper limit
	plt.ylim(min(prices) * 0.99, max(prices) * 1.01)
	# save file using symbol, country and trading date as file name
	plt.savefig(symbol + '_' + country + '_' + tradingDate + '.pdf')
	plt.close(fig)

def epochTimeConversion(epochTimes, tzOrg, tzFin):
	'''
	convert epoch time using original and final time zone
	'''
	final_time = []
	for epochTime in epochTimes:
		# convert epoch time into UTC time with original time zone info
		org_moment = datetime.datetime.utcfromtimestamp(epochTime).replace(tzinfo = tzOrg)
		# convert UTC time into local time with final time zone info
		fin_moment = org_moment.astimezone(tzFin)
		final_time.append(fin_moment)
	return final_time

def getCompanyName(symbol, country):
	'''
	return company name using its stock symbol and country code
	'''

	# get bloomberg quote search result
	url = 'http://www.bloomberg.com/quote/' + symbol + ':' + country
	content = urllib2.urlopen(url).read()

	# create beautifulsoup object
	soup = BeautifulSoup(content, 'html.parser')

	# get tag with class = 'name', remove leading and trailing spaces
	companyName = soup.find('h1', {'class': 'name'}).string.strip()

	return companyName


if __name__ == '__main__':
	# get stock info from stocks of interest
	f = open('stocksOfInterest.txt')

	# create stockInfo array containing stock symbol and country code
	# stockInfo -> [[symbol1, countryCode1], [symbol2, countryCode2], ..., [symbolX, countryCodeX]]
	stockInfo = f.read().split('\n')

	f.close()

	# iterate each stockInfo
	for info in stockInfo:
		# get symbol and country code
		symbol, country = info.split()
		companyName = getCompanyName(symbol, country)
		dailyPrice(symbol, country, companyName)