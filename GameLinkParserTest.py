from HTMLParser import *
from GameLinkParser import *
import unittest
from GameLinkParserTestConstants import *

class GameLinkParserTest(unittest.TestCase):
    def testgamesForOneDay(self):
        self.assertEqual(GameLinkParser.getLinks("20170103", "20170103"), ONEDAY, msg = "Gets links for one day" )

    def testgamesWithinOneMonth(self): #None
        self.assertCountEqual(GameLinkParser.getLinks("20170103", "20170130"), LESSONEMONTH, msg = "Gets links for one month")

    def testgamesForSelectedTeam(self):
        self.assertEqual(GameLinkParser.getLinks("20170104", "20170130", ["MEM"]), SELECTEDTEAM, msg = "Gets links for one team")

    def testgamesForSelectedTeams(self): #None
        self.assertCountEqual(GameLinkParser.getLinks("20170104", "20170130", ["MEM", "MIA"]), SELECTEDTEAMS, msg = "Gets links for teams")

    def testgamesForMultipleMonths(self): #None
        self.assertCountEqual(GameLinkParser.getLinks("20131004", "20140416", ["MEM"]), MULTIPLEMONTHS, msg = "Gets links for multiple months" )

    # def gamesForMultipleYears(self):
    #     pass


if __name__ == '__main__':
    unittest.main()