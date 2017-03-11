class SingleGameDataScraper(object):
    DATAFIELDS = ['mp', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta',
                  'orb', 'drb', 'ast', 'stl', 'blk', 'tov',
                  'pf', 'pts', 'plus_minus']
    def __init__ (self, link):
        self.link =link
        self.html = HTMLParser.parse(link)
        self.home, self.away, self.date, self.homewin = self.initaliseGame()

    def generate(self):
        homeTeamBoxScore = self.basicTableText(self.html, self.home)
        awayTeamBoxScore = self.basicTableText(self.html, self.away)

        return {'homePlayerData': self.PlayerData(homeTeamBoxScore, self.home),
                'homeTeamData': self.TeamData(homeTeamBoxScore, self.home),
                'awayPlayerData': self.PlayerData(awayTeamBoxScore, self.away),
                'awayTeamData': self.TeamData(awayTeamBoxScore, self.away)
                }

    ### Private Methods ###
    def initialiseGame(self):
        home, away= self.teams()
        date = self.link[-17:-9]
        win = self.homeWin()
        return home, away, date, win

    def homeWin(self):
        home = self.link(-8: -5)
        loserStart = self.html.find("<a", self.html.find("loser"))
        loserEnd = self.html.find("</a>", loserStart)
        loserTeam = self.insideValue(self.html[loserStart + 1: loserEnd +1], '')
        if home == loserTeam:
            return False
        else:
            return True
        
    def basicTableText(self, text, team):
        box_basic_index = text.find(self.basicTableID(team)) # id= box_lac_basic
        start = text.find("<tr>", box_basic_index)
        end = text.find("</tfoot>", start)
        return text[start:end]

    def basicTableID(self, team): 
        return 'box_' + str(team).lower() + '_basic'

    def insideValue(self, text, value):
        start = text.find(">", text.find(value))
        end = text.find("<", start)
        return text[start+1: end]

    def statLineData(self, data, team):
        name= self.insideValue(data, '')
        
        if data.count("Did Not") ==1:
            return

        else:
            dataDict = {'opp': self.home if team == self.away else self.away}
            for field in DATAFIELDS:
                dataDict[field] = self.insideValue(data, 'data-stat="' + field)
                
            return [name, dataDict]

    def PlayerData(self, boxScore, team):
        boxScoreList = []
        while boxScore.count("<a") >0: 
            firstLink = boxScore.find("<a")
            dataIndex = boxScore.find("<td", firstLink)
            endIndex = boxScore.find("</tr>", firstLink) -1
            playerData = boxScore[firstLink: endIndex]
            boxScoreList.append(self.statLineData(playerData, team))
            boxScore = boxScore[endIndex+1: ]
        for i in boxScoreList:
            if i ==None:
                  boxScoreList.remove(i) 

        return boxScoreList

    def TeamData(self, boxScore, team):
        teamIndex = boxScore.rfind(">Team Totals")
        singleEndIndex = boxScore.find("</tr>", teamIndex) -1
        teamData = boxScore[teamIndex-1: singleEndIndex]
        return self.statLineData(teamData, team)

