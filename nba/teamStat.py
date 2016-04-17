import urllib2, os
from bs4 import BeautifulSoup

'''
get one NBA team stat or query all NBA teams stats
'''

def teamStat(acronym):
	'''
	get NBA team stat using team acronym
	'''

	# source page
	url = 'http://espn.go.com/nba/team/schedule/_/name/' + acronym
	content = urllib2.urlopen(url).read()
	# create soup object
	soup = BeautifulSoup(content, 'html.parser')

	# get raw scores, opponents, statuses (home or away) and results (win or lose)
	rawScores = soup.find_all('li', {'class': 'score'})
	rawOpponents = soup.find_all('li', {'class': 'team-name'})
	rawStatuses = soup.find_all('li', {'class': 'game-status'}, string = ['vs', '@'])
	rawResults = soup.find_all('li', {'class': 'game-status'}, string = ['W', 'L'])

	# clean raw data and get scores, opponents, statuses and results
	scores = [score.find_all('a')[0].string for score in rawScores]
	opponents = [opponent.find_all('a')[0].get('href').split('/')[-2].upper() for opponent in rawOpponents]
	statuses = []
	for status in rawStatuses:
		if status.string == 'vs':
			statuses.append('Home') # change 'vs' into 'Home'
		else:
			statuses.append('Away') # change '@' into 'Away'
	results = [result.find_all('span')[0].string for result in rawResults]

	# initialise home win, home lose, away win and away lose counters
	HomeW = 0
	HomeL = 0
	AwayW = 0
	AwayL = 0

	# games go to OT
	OTMatches = 0
	# number of OTs
	OTs = 0

	# total points scored and lost
	pointsScored = 0
	pointsLost = 0

	# get 
	for i in range(len(scores)):
		score1, tmp = scores[i].split('-')
		tmp = tmp.split(' ')
		if len(tmp) == 2:
			# count games go to OT
			OTMatches += 1
			# count number of OTs
			if tmp[1] == 'OT':
				OTs += 1
			else:
				OTs += int(tmp[1][0])
		score2 = tmp[0]

		# convert score in str into int format
		score1, score2 = int(score1), int(score2)

		# update points of teams based on game result
		if results[i] == 'W':
			points, pointsOppo = score1, score2
		else:
			points, pointsOppo = score2, score1

		# update total points scored and lost
		pointsScored += points
		pointsLost += pointsOppo

		# update home win, home lose, away win and away lose counters based on status and result
		if statuses[i] == 'Home':
			if results[i] == 'W':
				HomeW += 1
			else:
				HomeL += 1
		else:
			if results[i] == 'W':
				AwayW += 1
			else:
				AwayL += 1

	# summarised win and lose result
	WL = str(HomeW + AwayW) + 'W' + str(HomeL + AwayL) + 'L'
	# win and lost (home)
	HomeWL = str(HomeW) + 'W' + str(HomeL) + 'L'
	# win and lost (away)
	AwayWL = str(AwayW) + 'W' + str(AwayL) + 'L'
	# average points scored and lost
	pointsScoredAvg = round(float(pointsScored) / len(scores), 2)
	pointsLostAvg = round(float(pointsLost) / len(scores), 2)

	# create summary content
	summary = 'Total: ' + WL + ' Home: ' + HomeWL + ' Away: ' + AwayWL + '\n' + 'Points scored per match: ' + str(pointsScoredAvg) + '\n' + 'Points lost per match: ' + str(pointsLostAvg) + '\n' + 'OT matches: ' + str(OTMatches) + ', Number of OTs: ' + str(OTs) + '\n\n'

	# write summary content to txt file
	f = open('teams/' + acronym + '.txt', 'w+')
	f.write(summary)
	f.close()

	# write stat for each game to txt file
	f = open('teams/' + acronym + '.txt', 'a')
	for i in range(len(scores)):
		entry = opponents[i] + '\t' + statuses[i] + '\t' + results[i] + '\t' + scores[i] + '\n'
		f.write(entry)
	f.close()

def queryAll():
	'''
	get all teams stat and save to txt files in a folder
	'''

	# check if folder exists
	if not os.path.exists('teams'):
			os.makedirs('teams')	

	# getting all team acronyms
	f = open('acronyms.txt')
	acronyms = f.read().split('\n')
	f.close()

	# iterate all acronyms and save team stat to files
	for acronym in acronyms:
		teamStat(acronym)

if __name__ == '__main__':
	queryAll()

# teamStat('gs')