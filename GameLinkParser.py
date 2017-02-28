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

	# self.scrapeLinks()

	@classmethod
	def getLinks(cls, start, end, teams=[]):
		return GameLinkParser(start, end, teams).scrapeLinks()


	def scrapeLinks(self):
		firstYear, firstMonth, firstDay = self.dateSplit(self.startDate)
		lastYear, lastMonth, lastDay = self.dateSplit(self.endDate)
		games = []
		games.extend(self.scrapePartialMonth(self.startDate,
											 firstYear + firstMonth + str(GameLinkParser.DAYSINMONTH[int(firstMonth)])))
		games.extend(self.scrapePartialMonth(lastYear + lastMonth + "01", self.endDate))

		for month in self.fullMonthsToScrape():
			games.extend(self.scrapeMonth(month))
			print (games)
		return games

	def fullMonthsToScrape(self):
		firstYear, firstMonth, firstDay = self.dateSplit(self.startDate)
		lastYear, lastMonth, lastDay = self.dateSplit(self.endDate)
		monthsToScrape = []
		print (firstYear + "_" + lastYear)
		if firstYear == lastYear:
			for month in range(int(firstMonth) + 1, int(lastMonth)):
				monthsToScrape.append(firstYear + self.numToMonth(month) + "01")
		else:
			for month in range(int(firstMonth) + 1, 12 + 1):
				monthsToScrape.append(firstYear + self.numToMonth(month) + "01")

			for month in range(1, int(lastMonth)):
				monthsToScrape.append(firstYear + self.numToMonth(month) + "01")

			for year in range(int(firstYear) + 1, int(lastYear)):
				for month in range(0, 12):
					monthsToScrape.append(str(year) + self.numToMonth(month) + "01")
		return list(set(monthsToScrape))

	def scrapePartialMonth(self, start, end):
		result = []
		table = self.gameTableMonth(start, end)
		while table.find("</tr>") != -1:
			trStart = table.find("<tr")
			trEnd = table.find("</tr>") + 5
			tableRow = table[trStart: trEnd]
			result.append(self.gameLink(tableRow))
			table = table[trEnd:]
		return result

	def scrapeMonth(self, startDay):
		startYear, startMonth, startDate = self.dateSplit(startDay)
		endDate = str(GameLinkParser.DAYSINMONTH[int(startMonth)])
		lastDay = startYear + startMonth + endDate
		return self.scrapePartialMonth(startDay, lastDay)

	def gameTableMonth(self, start, end): ## TODO: cut table to between dates
		body = HTMLParser.parse(self.linkForMonth(start))
		tableStart = body.find('id="div_schedule"')
		tbodyStart = body.find("<tbody>", tableStart)
		tbodyend = body.find("</tbody>", tbodyStart)
		return body[tbodyStart:tbodyend]

	def gameLink(self, row):  # csk="201311010ATL"
		if self.teamCheck(row):
			start = row.find('csk="')
			end = row.find('"', start +6)
			return self.linkForGame(row[start + 5: end - 4], row[end - 3: end])

	def teamCheck(self, row):  # href="/teams/ATL/2014.html"
		if len(self.teams) == 0:
			return True
		else:
			team1, team2 = teams(row)

			if (team1 in self.teams) or (team2 in self.teams):
				return True
			return False

	def teams(self, row):  # href="/teams/ATL/2014.html" and href="/teams/TOR/2014.html"
		teamIndex1 = row.find("teams/") + 6
		teamIndex2 = row.rfind("teams/") + 6
		team1 = row[teamIndex1: teamIndex1 + 3]
		team2 = row[teamIndex2: teamIndex2 + 3]
		return team1, team2

	def linkForGame(self, date, homeTeam):
		return "http://www.basketball-reference.com/boxscores/{0}0{1}.html". \
			format(date, homeTeam)

	def linkForMonth(self, date):
		year = date[:4]
		month = date[4:6]
		return "http://www.basketball-reference.com/leagues/NBA_{0}_games-{1}.html". \
			format(year, GameLinkParser.DATE[int(month)])

	def dateSplit(self, date):
		return date[:4], date[4:6], date[6:]  # year, month, day

	def numToMonth(self, month):
		if month > 9:
			return str(month)

		else:
			return "0{0}".format(str(month))


def main():
	links = GameLinkParser.getLinks("20170103", "20170103")
	print (links)

if __name__ == '__main__':
	main()
