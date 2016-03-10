import pytz
import datetime
import time
import urllib2
import json
import os
from bs4 import BeautifulSoup

# e.g. http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=MLB&period=20160307

def today(league):
	yyyymmdd = int(datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%Y%m%d"))
	games = []
	
	try:
		url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=%s&period=%d'
		url = url % (league, yyyymmdd)
		# print url
		content = urllib2.urlopen(url).read().replace('shsMSNBCTicker.loadGamesData(', '').replace(');', '')
		data = json.loads(content)

		games = data['games']
		for game in games:
			soup = BeautifulSoup(game, 'html.parser')

			h_name, h_summary, h_score = eachTeam(soup, 'home-team')
			v_name, v_summary, v_score = eachTeam(soup, 'visiting-team')

			state = soup.find('gamestate')
			# needs modification
			status = state.get('status')

			if status == 'In-Progress':

				clock = state.get('display_status1')
				clock_section = state.get('display_status2')

				# os.system('clear')

				print h_name + '(' + h_summary + ')', 'vs', v_name + '(' + v_summary + ')'
				# if status != 'Pre-Game':
				print
				print 'Team' + '\t' + '1\t2\t3\t4\t\tT'
				print h_score
				print v_score
				print

				if status == 'Final':
					print status
				elif status == 'Pre-Game':
					print status, 'Game @', clock
				else:
					print status, clock, clock_section
				print '*' * 50

	except Exception, e:
		print e

def eachTeam(soup, team):
	team = soup.find(team)

	name = team.get('display_name')
	nickname = team.get('nickname')
	alias = team.get('alias').upper()
	name = name + ' ' + nickname

	team_record = team.find('team-record')
	summary =  team_record.get('wins') + 'W' + team_record.get('losses') + 'L'

	quarter_score_tmp = team.find_all('score')
	score = quarter_score_tmp[-1].get('value')
	tmp = [q.get('value') for q in quarter_score_tmp[:-1]]
	tmp = tmp + ['-'] * (4 - len(tmp))
	quarter_score = alias + '\t\t' + '\t'.join(tmp) + '\t|\t' + score

	# reversed for update
	gz_image = team.find('team-logo').get('gz-image')
	link = team.find('team-logo').get('link')

	return name, summary, quarter_score



today('NBA')
# time.sleep(10)

# for league in ['NFL', 'MLB', 'NBA', 'NHL']:
#   print today(league)