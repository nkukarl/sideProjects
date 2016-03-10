import urllib2, os
from bs4 import BeautifulSoup

def queryAll():
	if not os.path.exists('teams'):
			os.makedirs('teams')	

	f = open('acronyms.txt')
	acronyms = f.read().split('\n')
	f.close()

	for acronym in acronyms:
		teamStat(acronym)

def teamStat(acronym):
	url = 'http://espn.go.com/nba/team/schedule/_/name/' + acronym
	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content, 'html.parser')
	rawScores = soup.find_all('li', {'class': 'score'})
	rawOpponents = soup.find_all('li', {'class': 'team-name'})
	rawStatuss = soup.find_all('li', {'class': 'game-status'}, string = ['vs', '@'])
	rawResults = soup.find_all('li', {'class': 'game-status'}, string = ['W', 'L'])

	scores = [score.find_all('a')[0].string for score in rawScores]
	opponents = [opponent.find_all('a')[0].get('href').split('/')[-2].upper() for opponent in rawOpponents]
	statuss = []
	for status in rawStatuss:
		if status.string == 'vs':
			statuss.append('Home')
		else:
			statuss.append('Away')
	results = [result.find_all('span')[0].string for result in rawResults]

	HomeW = 0
	HomeL = 0
	AwayW = 0
	AwayL = 0

	OTMatches = 0
	OTs = 0

	pointsScored = 0
	pointsLost = 0

	for i in range(len(scores)):
		score1, tmp = scores[i].split('-')
		tmp = tmp.split(' ')
		if len(tmp) == 2:
			OTMatches += 1
			if tmp[1] == 'OT':
				OTs += 1
			else:
				OTs += int(tmp[1][0])
		score2 = tmp[0]

		score1, score2 = int(score1), int(score2)

		if results[i] == 'W':
			points, pointsOppo = score1, score2
		else:
			points, pointsOppo = score2, score1

		pointsScored += points
		pointsLost += pointsOppo

		if statuss[i] == 'Home':
			if results[i] == 'W':
				HomeW += 1
			else:
				HomeL += 1
		else:
			if results[i] == 'W':
				AwayW += 1
			else:
				AwayL += 1

	WL = str(HomeW + AwayW) + 'W' + str(HomeL + AwayL) + 'L'
	HomeWL = str(HomeW) + 'W' + str(HomeL) + 'L'
	AwayWL = str(AwayW) + 'W' + str(AwayL) + 'L'
	pointsScoredAvg = round(float(pointsScored) / len(scores), 2)
	pointsLostAvg = round(float(pointsLost) / len(scores), 2)

	summary = 'Total: ' + WL + ' Home: ' + HomeWL + ' Away: ' + AwayWL + '\n' + 'Points scored per match: ' + str(pointsScoredAvg) + '\n' + 'Points lost per match: ' + str(pointsLostAvg) + '\n' + 'OT matches: ' + str(OTMatches) + ', Number of OTs: ' + str(OTs) + '\n\n'

	f = open('teams/' + acronym + '.txt', 'w+')
	f.write(summary)
	f.close()

	f = open('teams/' + acronym + '.txt', 'a')
	for i in range(len(scores)):
		entry = opponents[i] + '\t' + statuss[i] + '\t' + results[i] + '\t' + scores[i] + '\n'
		f.write(entry)
	f.close()

queryAll()

# teamStat('gs')