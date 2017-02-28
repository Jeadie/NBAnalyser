from HTMLParser import *
class GameLinkParser(object):
	DATE = {1: "january", 2: "february", 3: "march", 4: "april",
			5: "may", 6: "june", 7: "july", 8: "august", 9: "september",
			10: "october", 11: "november", 12: "december"}
	DAYSINMONTH = {1: 31, 2: 29, 3: 31, 4: 30,
				   5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
				   10: 31, 11: 30, 12: 31}
	def __init__(self, startdate, enddate, teams=[]):
		self.startDate = startdate
		self.endDate = enddate
		self.teams = teams
		self.games = []
		self.scrapeLinks()

	@classmethod
	def getLinks(cls, start, end, teams = []):
		LinkParser = cls(start, end, teams)
		return self.games

	def scrapeLinks(self):
		firstYear, firstMonth, firstDay = dateSplit(self.startDate)
		lastYear, lastMonth, lastDay = dateSplit(self.endDate)
		games = []
		games.extend(self.scrapePartialMonth(self.startDate ,
									 firstYear + firstMonth + DAYSINMONTH[int(firstMonth)]))
		games.extend(self.scrapePartialMonth(lastYear + lastMonth + "01", self.endDate))

		for month in self.fullMonthsToScrape():
			games.extend(self.scrapeMonth(month))
		self.games = games

	def fullMonthsToScrape(self):
		firstYear, firstMonth, firstDay = dateSplit(self.startDate)
		lastYear, lastMonth, lastDay = dateSplit(self.endDate)
		monthsToScrape = []

		for month in range(firstMonth + 1, 12 + 1):
			monthsToScrape.extend(firstYear + numToMonth(month) + "01")

		for month in range(1, lastMonth):
			monthsToScrape.extend(firstYear + numToMonth(month) + "01")

		for year in range(firstYear + 1, lastYear):
			for month in range(0, 12):
				monthsToScrape.extend(str(year) + numToMonth(month) + "01")
		return list(set(monthsToScrape))

	def scrapePartialMonth(self, start, end):
		result = []
		table = self.gameTableMonth(month)

		firstGame = table.rfind("<tr>", 0, table.find('csk="{0}'.format(start)))
		lastGame = table.find("</tr>", 'csk="{0}'.format(end)) + 5

		table= table[firstGame: lastGame]
		while table.find("</tr>") != -1:
			trStart = table.find("<tr")
			trEnd = table.find("</tr>") + 5
			tableRow = table[trStart: trEnd]
			result.append(self.gameLink(tableRow))
			table = table[trEnd:]
		return result

	def scrapeMonth(self, startDay):
		startYear, startMonth, startDate = dateSplit(startDay)
		lastDay = startYear + startMonth + start(DAYSINMONTH[int(startMonth)])
		return self.scrapePartialMonth(startDay, lastDay)

	def gameTableMonth(self, month):
		body = HTMLParser.parse(self.linkForMonth(month))
		tableStart = body.find('id="div_schedule"')
		tbodyStart = body.find("<tbody>", tableStart)
		tbodyend = body.find("</tbody>", tbodyStart)
		return body[tbodyStart:tbodyend]

	def gameLink(self, row): #csk="201311010ATL"
		if self.teamCheck(row):
			start = row.find('csk="')
			end = row.find('"', start)
			return linkforGame(row[start + 5: end-3], row[end-3: end])

	def teamCheck(self, row): #href="/teams/ATL/2014.html"
		if len(self.teams) == 0:
			return True
		else:
			team1, team2 = teams(row)

			if (team1 in self.teams) or (team2 in self.teams):
				return True
			return False

	def teams(self, row): #href="/teams/ATL/2014.html" and href="/teams/TOR/2014.html"
		teamIndex1 = row.find("teams/") + 6:
		teamIndex2 = row.rfind("teams/") + 6
		team1 = row[teamIndex1: teamIndex1 + 3]
		team2 = row[teamIndex2: teamIndex2 + 3]
		return team1, team2

	def linkforGame(date, homeTeam):
		return "http://www.basketball-reference.com/boxscores/{0}0{1}.html".\
			format(date, homeTeam)

	def linkforMonth(self, date):
		year = date[:4]
		month = date[4:6]
		return "http://www.basketball-reference.com/leagues/NBA_{0}_games-{1}.html".\
			format(year, Date[month])

	def dateSplit( date):
		return date[:4], date[4:6], date[6:] # year, month, day


	def numToMonth(month):
		if month > 9:
			return str(month)

		else:
			return "0{0}".format(str(month))



