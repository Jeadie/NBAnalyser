from HTMLParser import *
from GameLinkParser import *
import unittest


class GameLinkParserTest(unittest.TestCase):
    def setUp(self):
        "http://www.basketball-reference.com/boxscores/{0}0{1}.html". \
            format(date, homeTeam)

    def gamesForOneDay(self):
        self.assertequal(GameLinkParser.getLinks("20170103", "20170103"), LINKSFORONEGAME, msg = "Gets links for one day" )

    def gamesWithinOneMonth(self):
        self.assertEqual(GameLinkParser.getLinks("20170103", "20170203"), LINKSFORONEMONTH, msg = "Gets links for one month")

    def gamesForSelectedTeam(self):
        pass

    def gamesForSelectedTeams(self):
        pass

    def gamesForMultipleMonths(self):
        pass

    def gamesForMultipleYears(self):
        pass


if __name__ == '__main__':
    unittest.main()
