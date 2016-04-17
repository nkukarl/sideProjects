import pytz, datetime, time, urllib2, json, os
from bs4 import BeautifulSoup

'''
example on how to use source page
http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=MLB&period=20160307
'''

def today(league):
	'''
	get today's game of current league
	'''

	# today's date using US/Pacific time zone
	yyyymmdd = int(datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%Y%m%d"))
	games = []
	
	try:
		# source page
		url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=%s&period=%d'
		url = url % (league, yyyymmdd)
		# print url
		content = urllib2.urlopen(url).read().replace('shsMSNBCTicker.loadGamesData(', '').replace(');', '')
		# get json object
		data = json.loads(content)

		# get games from 'games' attribute of data
		games = data['games']
		for game in games:
			soup = BeautifulSoup(game, 'html.parser')

			# home team, home summary and home score
			h_name, h_summary, h_score = eachTeam(soup, 'home-team')
			v_name, v_summary, v_score = eachTeam(soup, 'visiting-team')

			# get game state and status
			state = soup.find('gamestate')
			status = state.get('status')

			# get clock info
			clock = state.get('display_status1')
			clock_section = state.get('display_status2')

			# os.system('clear')

			# display home and visiting team info
			print h_name + '(' + h_summary + ')', 'vs', v_name + '(' + v_summary + ')'
			print
			# formulate score
			print 'Team' + '\t' + '1\t2\t3\t4\t\tT'
			print h_score
			print v_score
			print

			# print game status
			if status == 'Final': # game has finished
				print status
			elif status == 'Pre-Game': # if game has not started, show start time
				print status, 'Game @', clock
			else:
				print status, clock, clock_section # game in progress
			print '*' * 60

	except Exception, e:
		print e

def eachTeam(soup, team):
	'''
	get team info
	'''
	# get info from soup using team name as keyword
	team = soup.find(team)

	# get team names
	name = team.get('display_name')
	nickname = team.get('nickname')
	alias = team.get('alias').upper()
	name = name + ' ' + nickname

	# get team record (win and lose info)
	team_record = team.find('team-record')
	summary =  team_record.get('wins') + 'W' + team_record.get('losses') + 'L'

	# find quarter score info
	quarter_score_tmp = team.find_all('score')

	# find score info
	score = quarter_score_tmp[-1].get('value')

	# formulate quarter score
	tmp = [q.get('value') for q in quarter_score_tmp[:-1]]
	# if quarter score exits, use quarter score
	# otherwise use '-'
	tmp = tmp + ['-'] * (4 - len(tmp))
	quarter_score = alias + '\t\t' + '\t'.join(tmp) + '\t|\t' + score

	# getting team logo and link
	# more features might be added
	gz_image = team.find('team-logo').get('gz-image')
	link = team.find('team-logo').get('link')

	return name, summary, quarter_score


if __name__ == '__main__':
	today('NBA')