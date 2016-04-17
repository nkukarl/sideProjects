import urllib2
from bs4 import BeautifulSoup

'''
get NBA teams acronyms and full names
'''

# source page
index = 'http://espn.go.com/nba/teams'

content = urllib2.urlopen(index).read()

soup = BeautifulSoup(content, 'html.parser')

# find all a tags with class = 'bi'
aTags = soup.find_all('a', {'class': 'bi'})

# get url for each team, team name and acronym can be found in url
links = [aTag.get('href') for aTag in aTags]

acronyms = []
fullNames = []

for l in links:
	# split url using '/'
	acronym, fullName = l.split('/')[-2:]
	# convert acronym into upper case
	acronyms.append(acronym.upper())
	# replace '-' in team name by ' ' and convert into title case
	fullNames.append(fullName.replace('-', ' ').title())

# create acronym -> name map
MAP = dict(zip(acronyms, fullNames))

# sort acronyms
acronyms.sort()

# recreate team full name using sorted acronyms and MAP
fullNames = [MAP[acronym] for acronym in acronyms]

# save acronyms and fullnames to txt files
f = open('acronyms.txt', 'w+')
f.write('\n'.join(acronyms))
f.close()

f = open('fullNames.txt', 'w+')
f.write('\n'.join(fullNames))
f.close()