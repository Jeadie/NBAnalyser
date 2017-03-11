from HTMLParser import *


class GameLinkParser(object):
	DATE = {1: "january", 2: "february", 3: "march", 4: "april",
			5: "may", 6: "june", 7: "july", 8: "august", 9: "september",
			10: "october", 11: "november", 12: "december"}
	DAYSINMONTH = {1: 31, 2: 29, 3: 31, 4: 30,
				   5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
				   10: 31, 11: 30, 12: 31}

	MONTHSWITHNOGAMES = [7,8,9]

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

		if firstYear == lastYear and firstMonth == lastMonth:
			games.extend(self.scrapePartialMonth(self.startDate, self.endDate))

		else:
			games.extend(self.scrapePartialMonth(self.startDate,
												 firstYear + firstMonth + str(
													 GameLinkParser.DAYSINMONTH[int(firstMonth)])))
			games.extend(self.scrapePartialMonth(lastYear + lastMonth + "01", self.endDate))

			for month in self.fullMonthsToScrape():
				games.extend(self.scrapeMonth(month))

		games = list(filter(None, games))
		return games

	def fullMonthsToScrape(self):
		firstYear, firstMonth, firstDay = self.dateSplit(self.startDate)
		lastYear, lastMonth, lastDay = self.dateSplit(self.endDate)
		monthsToScrape = []
		if firstYear == lastYear:
			for month in range(int(firstMonth) + 1, int(lastMonth)):
				if month not in self.MONTHSWITHNOGAMES:
					monthsToScrape.append(firstYear + self.numToMonth(month) + "01")
		else:
			for month in range(int(firstMonth) + 1, 12 + 1):
				if month not in self.MONTHSWITHNOGAMES:
					#print("month" + str(month) + "year" + firstYear)
					monthsToScrape.append(firstYear + self.numToMonth(month) + "01")

			for month in range(1, int(lastMonth)):
				if month not in self.MONTHSWITHNOGAMES:
					#print("month" + str(month) + "year" + lastYear)
					monthsToScrape.append(lastYear + self.numToMonth(month) + "01")

			for year in range(int(firstYear) + 1, int(lastYear)):
				for month in range(1, 13):
					if month not in self.MONTHSWITHNOGAMES:
						#print("month" + str(month) + "year" + str(year))
						monthsToScrape.append(str(year) + self.numToMonth(month) + "01")
		return list(set(monthsToScrape))

	def scrapePartialMonth(self, start, end):
		result = []
		#print("Start: " + start + " and End: " + end)
		table = self.gameTableMonth(start, end)
		while table.find("</tr>") != -1:
			trStart = table.find("<tr")
			trEnd = table.find("</tr>") + 5
			tableRow = table[trStart: trEnd]
			result.append(self.gameLink(tableRow))
			table = table[trEnd:]
		result = list(filter(None, result))
		return result

	def scrapeMonth(self, startDay):
		startYear, startMonth, startDate = self.dateSplit(startDay)
		endDate = str(GameLinkParser.DAYSINMONTH[int(startMonth)])
		lastDay = startYear + startMonth + endDate
		return self.scrapePartialMonth(startDay, lastDay)

	def gameTableMonth(self, start, end):
		body = HTMLParser.parse(self.linkForMonth(start))
		firstGame = body.find('csk="' + start)
		if firstGame == -1:
			tableStart = body.find("<tr", body.find('Date'))
		else:
			tableStart = body.rfind("<tr", 0, firstGame)
		lastGame = body.rfind('csk="' + end)
		if lastGame == -1:
			tableEnd = body.rfind("</tr>", firstGame, body.find("</tbody>", firstGame))
		else:
			tableEnd = body.find("</tr>", lastGame) + 5
		return body[tableStart:tableEnd]

	def gameLink(self, row):  # csk="201311010ATL"
		if self.teamCheck(row):
			start = row.find('csk="')
			end = row.find('"', start + 6)
			return self.linkForGame(row[start + 5: end - 4], row[end - 3: end])

	def teamCheck(self, row):  # href="/teams/ATL/2014.html"
		if len(self.teams) == 0:
			return True
		else:
			team1, team2 = self.teamsFromRow(row)

			if (team1 in self.teams) or (team2 in self.teams):
				return True
			return False

	def teamsFromRow(self, row):  # href="/teams/ATL/2014.html" and href="/teams/TOR/2014.html"
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
		if int(month) > 9:
			year = str(int(year) + 1)
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
	links = GameLinkParser.getLinks("20170104", "20170130", ["MEM"])
	#links1 = GameLinkParser.getLinks("20170104", "20170130", ["MEM", "MIA"])

	print (links)
	print(len(links))


	#print(links1)
	#print(len(links1))

if __name__ == '__main__':
	main()
