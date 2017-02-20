from HTMLParser import *
class GameSetScrapper(object):
	DATE = {1: "january", 2: "february", 3: "march", 4: "april",
			5: "may", 6: "june", 7: "july", 8: "august", 9: "september",
			10: "october", 11: "november", 12: "december"}
	MONTHDAYS = {1: 31, 2: 29, 3: 31, 4: 30,
			5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
			10: 31, 11: 30, 12: 31}
    def __init__(self, startdate, enddate, teams=[]):
        self.startDate = startdate
        self.endDate = enddate
        self.teams = teams

    @classmethod
    def all(cls, startDate, endDate):
        return cls(startDate, endDate)

    @classmethod
    def team(cls, startDate, endDate, team):
            return cls(startDate, endDate, [team])

    @classmethod
    def teams(cls, startDate, endDate, teams):
            return cls(startDate, endDate, teams)

    @classmethod
    def season(cls, season):
            startDate = str(season) + "1010"
            endDate = str(season + 1) + "0620"
            return cls(startDate, endDate)

    def scrape(self):


    def scrapeMonth(self, start, end):
        result = []
        body = HTMLParser.parse(self.linkForMonth(start))
        tableStart = body.find('id="div_schedule"')
        tbodyStart = body.find ("<tbody>", tableStart)
        tbodyend = body.find("</tbody>", tbodyStart)
        table= body[tbodyStart:tbodyend]

        while table.find("</tr>") != -1:
            trStart = table.find("<tr")
            trEnd = table.find("</tr>") + 5
            row = table[trStart: trEnd]
            result.append(self.gameLink(row, start, end))
            table= table[trEnd: ]

    def gameLink(self, row, start, end):
        if self.teamCheck(row):
            start = row.find('csk="')
            end = row.find('"', start)
            return self.linkforGame(row[start + 5: end-3], row[end-3: end])
        return

    def teamCheck(self, row):
        if len(self.teams) == 0:
            return True
        else:
            team1, team2 = self.teams(row)

            if (team1 in self.teams) or (team2 in self.teams):
                return True
            return False

    def teams(self, row):
        teamIndex1 = row.find("teams/") + 6:
        teamIndex2 = row.rfind("teams/") + 6
        team1 = row[teamIndex1: teamIndex1 + 3]
        team2 = row[teamIndex2: teamIndex2 + 3]
        return team1, team2

def linkforGame(self, date, homeTeam):
        return "http://www.basketball-reference.com/boxscores/{0}0{1}.html".\
            format(date, homeTeam)

    def linkforMonth(self, date):
        year = date[:4]
        month = date[4:6]
        return "http://www.basketball-reference.com/leagues/NBA_{0}_games-{1}.html".\
            format(year, Date[month])

    def scrapeDate(self, date):
        body = HTMLParser.parse(self.linkForDate(date))

        if body.find("No games played on this date") == -1:
            return
        while

    def dateSplit(self, date):
        return date[:4], date[4:6], date[6:] # year, month, day


