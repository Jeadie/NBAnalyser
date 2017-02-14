import urllib.request as url
class SingleGameDataScraper(object):

    def __init__ (self, home, away, date):
        self.home = home
        self.away = away
        self.date = date
        self.dataFields = ['mp', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta',
                           'orb', 'drb', 'ast', 'stl', 'blk', 'tov',
                           'pf', 'pts', 'plus_minus']
        self.win = self.winner()

    def winner(self):
        return True
        
    def basicTableText(self, text, team):
        box_basic_index = text.find(self.basicTableID(team)) # id= box_lac_basic
        start = text.find("<tr>", box_basic_index)
        end = text.find("</tfoot>", start)
        return text[start:end]

    def basicTableID(self, team): 
        return 'box_' + str(team).lower() + '_basic'


    def RawtoCleanHTML(self, text):
        remove_list= ["\\n", "  ", "\\r", "\\t"]
        new_text= text
        for i in remove_list:
            new_text = new_text.replace(i, "")
        return new_text

    def boxScoreLink(self):
        return 'http://www.basketball-reference.com/boxscores/'+ self.date+ "0" + self.home + '.html'

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
            for field in self.dataFields:
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

    def bodyHtml(self):
        response = url.urlopen(self.boxScoreLink())
        html = self.RawtoCleanHTML(str(response.read()))
        return html[html.find("<body"): html.find("</body>")]
        
    def generate(self):
        html= self.bodyHtml()
        homeTeamBoxScore = self.basicTableText(html, self.home)
        awayTeamBoxScore = self.basicTableText(html, self.away)
        
        return {'homePlayerData': self.PlayerData(homeTeamBoxScore, self.home),
                'homeTeamData': self.TeamData(homeTeamBoxScore, self.home),
                'awayPlayerData': self.PlayerData(awayTeamBoxScore, self.away),
                'awayTeamData': self.PlayerData(awayTeamBoxScore, self.away)
                }
