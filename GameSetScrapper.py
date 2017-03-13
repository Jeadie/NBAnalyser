from GameLinkParser import *
from SingleGameDataScraper import *

class GameSetScrapper(object):
    DATE = {1: "january", 2: "february", 3: "march", 4: "april",
            5: "may", 6: "june", 7: "july", 8: "august", 9: "september",
            10: "october", 11: "november", 12: "december"}
    DAYSINMONTH = {1: 31, 2: 29, 3: 31, 4: 30,
                   5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
                   10: 31, 11: 30, 12: 31}

    def __init__(self, startdate, enddate, teams=[]):
        self.gameLinks = GameLinkParser.getLinks(startdate, enddate, teams)
        self.gameData = self.getGameData()

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

    def getGameData(self):
        gameData = []
        for link in self.gameLinks:
            print (link)
            gameData.append(SingleGameDataScraper(link).generate())
        return gameData

def main():
    Games = GameSetScrapper.all("20170104", "20170106")
    print(len(Games.gameData))
    print (Games.gameData[0]["awayTeamData"])
if __name__ == '__main__':
    main()
