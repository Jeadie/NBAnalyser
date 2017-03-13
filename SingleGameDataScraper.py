from HTMLParser import *


class SingleGameDataScraper(object):
    DATAFIELDS = ['mp', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta',
                  'orb', 'drb', 'ast', 'stl', 'blk', 'tov',
                  'pf', 'plus_minus']

    TEAMFIELDS = ['fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta',
                  'orb', 'drb', 'ast', 'stl', 'blk', 'tov',
                  'pf']

    def __init__(self, link):
        self.link = link
        self.html = HTMLParser().parse(link)
        self.home, self.away, self.homewin, self.date = self.initialiseGame()

    def generate(self):
        homeTeamBoxScore = self.basicTableText(self.html, self.home)
        awayTeamBoxScore = self.basicTableText(self.html, self.away)

        return {'homePlayerData': self.PlayerData(homeTeamBoxScore, self.home),
                'homeTeamData': self.TeamData(homeTeamBoxScore, self.home),
                'awayPlayerData': self.PlayerData(awayTeamBoxScore, self.away),
                'awayTeamData': self.TeamData(awayTeamBoxScore, self.away)
                }

    ### Private Methods ###
    def initialiseDate(self):
        return self.link[-17:-9]

    def winnerText(self, text):
        if "winner" in text:
            return True
        return False

    def findAwayTeam(self):
        awayTableIndex = self.html.find("<table")
        awayTeamIndex = self.html.find('id="box_', awayTableIndex)
        return (self.html[awayTeamIndex + 8 : awayTeamIndex + 8+ 3]).upper()

    def findHomeTeam(self):
        return self.link[-8:-5]

    def initialiseGame(self):
        return self.findAwayTeam(), self.findHomeTeam(), True, self.initialiseDate()

    def basicTableText(self, text, team):
        box_basic_index = text.find(self.basicTableID(team))  # id= box_lac_basic
        start = text.find("<tr>", box_basic_index)
        end = text.find("</tfoot>", start)
        return text[start:end]

    def basicTableID(self, team):
        return 'box_' + str(team).lower() + '_basic'

    def insideValue(self, text, value):
        start = text.find(">", text.find(value))
        end = text.find("<", start)
        return text[start + 1: end]

    def statLineData(self, data, team, player):
        name = self.insideValue(data, '')

        if data.count("Did Not") == 1:
            return

        else:
            dataDict = {} #{'opp': self.home if team == self.away else self.away}
            dataDict['name'] = name
            if player:
                for field in self.DATAFIELDS:
                    dataDict[field] = self.insideValue(data, 'data-stat="' + field)

            else:
                for field in self.TEAMFIELDS:
                    dataDict[field] = self.insideValue(data, 'data-stat="' + field)

            return dataDict

    def PlayerData(self, boxScore, team):
        boxScoreList = []
        while boxScore.count("<a") > 0:
            firstLink = boxScore.find("<a")
            dataIndex = boxScore.find("<td", firstLink)
            endIndex = boxScore.find("</tr>", firstLink) - 1
            playerData = boxScore[firstLink: endIndex]
            boxScoreList.append(self.statLineData(playerData, team, True))
            boxScore = boxScore[endIndex + 1:]
        for i in boxScoreList:
            if i == None:
                boxScoreList.remove(i)

        return boxScoreList

    def TeamData(self, boxScore, team):
        teamIndex = boxScore.rfind(">Team Totals")
        singleEndIndex = boxScore.find("</tr>", teamIndex) - 1
        teamData = boxScore[teamIndex + 1: singleEndIndex]
        teamLine = self.statLineData(teamData, team, False)
        del teamLine["name"]
        return teamLine

