import json, urllib2, pytz, datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def dailyPrice(symbol, country, companyName):

	url = 'http://www.bloomberg.com/markets/chart/data/1D/' + symbol + ':' + country
	response = urllib2.urlopen(url)
	data = json.load(response)

	datapoints = data['data_values']

	epochTimes = []
	prices = []

	for dp in datapoints:
		rawTime, price = dp
		epochTimes.append(rawTime // 1000)
		prices.append(price)

	est = pytz.timezone('US/Eastern')
	aest = pytz.timezone('Australia/Sydney')
	ctz = pytz.timezone('Asia/Urumqi')

	tzMAP = {'US': est, 'AU': aest, 'CH': ctz}
	currencyMAP = {'US': 'USD', 'AU': 'AUD', 'CH': 'CNY'}

	tzOrg = est
	tzFin = tzMAP[country]

	final_time = epochTimeConversion(epochTimes, tzOrg, tzFin)

	tradingDate = str(final_time[0])[:10]

	fig = plt.figure()
	plt.plot(final_time, prices, label = symbol + ':' + country)
	plt.xlabel('Time', size = 15)
	plt.ylabel('Stock price ' + '(' + currencyMAP[country] + ')', size = 15)
	plt.legend(loc = 1)
	plt.title(companyName + ' (' + tradingDate + ')', size = 15)
	plt.ylim(min(prices) * 0.99, max(prices) * 1.01)
	# plt.show()
	plt.savefig(symbol + '_' + country + '_' + tradingDate + '.pdf')
	plt.close(fig)

def epochTimeConversion(epochTimes, tzOrg, tzFin):
	final_time = []
	for epochTime in epochTimes:
		org_moment = datetime.datetime.utcfromtimestamp(epochTime).replace(tzinfo = tzOrg)
		fin_moment = org_moment.astimezone(tzFin)
		final_time.append(fin_moment)
	return final_time

def getCompanyName(symbol, country):
	url = 'http://www.bloomberg.com/quote/' + symbol + ':' + country
	content = urllib2.urlopen(url).read()

	soup = BeautifulSoup(content, 'html.parser')
	companyName = soup.find('h1', {'class': 'name'}).string.strip()

	return companyName

f = open('stocksOfInterest.txt')
symbol_country = f.read().split('\n')
f.close()

for c_s in symbol_country:
	symbol, country = c_s.split()
	companyName = getCompanyName(symbol, country)
	dailyPrice(symbol, country, companyName)