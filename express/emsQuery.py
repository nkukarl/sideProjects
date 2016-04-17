import urllib2
from bs4 import BeautifulSoup

form = 'mailNum=1184552078099&checkCode=792054'
url = 'http://www.ems.com.cn/ems/order/singleQuery_t'

req = urllib2.Request(url, form)
content = urllib2.urlopen(req).read()

soup = BeautifulSoup(content, 'html.parser')

print(soup)