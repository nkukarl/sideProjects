import urllib2
from bs4 import BeautifulSoup

index = 'http://espn.go.com/nba/teams'

content = urllib2.urlopen(index).read()

soup = BeautifulSoup(content, 'html.parser')

aTags = soup.find_all('a', {'class': 'bi'})
links = [aTag.get('href') for aTag in aTags]

acronyms = []
fullNames = []

for l in links:
	acronym, fullName = l.split('/')[-2:]
	acronyms.append(acronym.upper())
	fullNames.append(fullName.replace('-', ' ').title())

MAP = dict(zip(acronyms, fullNames))

acronyms.sort()

fullNames = [MAP[acronym] for acronym in acronyms]

f = open('acronyms.txt', 'w+')
f.write('\n'.join(acronyms))
f.close()

f = open('fullNames.txt', 'w+')
f.write('\n'.join(fullNames))
f.close()