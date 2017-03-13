class SingleGameDataScraper(unittest.TestCase):
    def setUp(self):
        LINK = "http://www.basketball-reference.com/boxscores/201701040CHO.html"
        RESULT  = [{'awayPlayerData':
                    [['Nicolas Batum', {'blk': '0', 'drb': '2', 'fg': '7', 'pf': '2', 'opp': 'OKC', 'tov': '2', 'orb': '1', 'stl': '0', 'ft': '13', 'fg3a': '5', 'plus_minus': '+6', 'mp': '36:17', 'fta': '15', 'fg3': '1', 'fga': '18', 'ast': '4'}],
                     ['Kemba Walker', {'blk': '0', 'drb': '2', 'fg': '5', 'pf': '1', 'opp': 'OKC', 'tov': '3', 'orb': '2', 'stl': '2', 'ft': '9', 'fg3a': '4', 'plus_minus': '+9', 'mp': '32:59', 'fta': '9', 'fg3': '1', 'fga': '13', 'ast': '9'}],
                     ['Michael Kidd-Gilchrist', {'blk': '1', 'drb': '9', 'fg': '7', 'pf': '4', 'opp': 'OKC', 'tov': '1', 'orb': '2', 'stl': '0', 'ft': '0', 'fg3a': '0', 'plus_minus': '+3', 'mp': '31:52', 'fta': '2', 'fg3': '0', 'fga': '9', 'ast': '0'}],
                     ['Marvin Williams', {'blk': '3', 'drb': '6', 'fg': '3', 'pf': '1', 'opp': 'OKC', 'tov': '1', 'orb': '2', 'stl': '0', 'ft': '1', 'fg3a': '3', 'plus_minus': '0', 'mp': '26:46', 'fta': '1', 'fg3': '1', 'fga': '9', 'ast': '1'}],
                     ['Roy Hibbert', {'blk': '2', 'drb': '1', 'fg': '0', 'pf': '5', 'opp': 'OKC', 'tov': '0', 'orb': '1', 'stl': '1', 'ft': '3', 'fg3a': '0', 'plus_minus': '-6', 'mp': '21:11', 'fta': '4', 'fg3': '0', 'fga': '1', 'ast': '0'}],
                     ['Frank Kaminsky', {'blk': '1', 'drb': '4', 'fg': '6', 'pf': '2', 'opp': 'OKC', 'tov': '2', 'orb': '2', 'stl': '2', 'ft': '3', 'fg3a': '5', 'plus_minus': '+18', 'mp': '24:14', 'fta': '4', 'fg3': '2', 'fga': '11', 'ast': '2'}],
                     ['Spencer Hawes', {'blk': '2', 'drb': '4', 'fg': '2', 'pf': '4', 'opp': 'OKC', 'tov': '1', 'orb': '0', 'stl': '2', 'ft': '2', 'fg3a': '3', 'plus_minus': '+10', 'mp': '23:49', 'fta': '2', 'fg3': '2', 'fga': '6', 'ast': '2'}],
                     ['Ramon Sessions', {'blk': '0', 'drb': '2', 'fg': '3', 'pf': '0', 'opp': 'OKC', 'tov': '1', 'orb': '0', 'stl': '0', 'ft': '2', 'fg3a': '2', 'plus_minus': '+2', 'mp': '15:01', 'fta': '3', 'fg3': '1', 'fga': '5', 'ast': '3'}],
                     ['Marco Belinelli', {'blk': '0', 'drb': '2', 'fg': '1', 'pf': '1', 'opp': 'OKC', 'tov': '0', 'orb': '0', 'stl': '0', 'ft': '5', 'fg3a': '1', 'plus_minus': '+8', 'mp': '14:42', 'fta': '6', 'fg3': '0', 'fga': '4', 'ast': '1'}],
                     ['Jeremy Lamb', {'blk': '1', 'drb': '1', 'fg': '3', 'pf': '1', 'opp': 'OKC', 'tov': '0', 'orb': '0', 'stl': '1', 'ft': '2', 'fg3a': '1', 'plus_minus': '+5', 'mp': '11:43', 'fta': '3', 'fg3': '1', 'fga': '4', 'ast': '3'}],
                     ['Treveon Graham', {'blk': '0', 'drb': '0', 'fg': '0', 'pf': '0', 'opp': 'OKC', 'tov': '0', 'orb': '0', 'stl': '0', 'ft': '0', 'fg3a': '0', 'plus_minus': '0', 'mp': '1:26', 'fta': '0', 'fg3': '0', 'fga': '0', 'ast': '0'}],
                     None],
                    'homePlayerData':
                        [['Steven Adams', {'blk': '1', 'drb': '8', 'fg': '8', 'pf': '5', 'opp': 'CHO', 'tov': '2', 'orb': '4', 'stl': '1', 'ft': '2', 'fg3a': '0', 'plus_minus': '-8', 'mp': '36:29', 'fta': '2', 'fg3': '0', 'fga': '10', 'ast': '3'}],
                         ['Victor Oladipo', {'blk': '0', 'drb': '1', 'fg': '7', 'pf': '5', 'opp': 'CHO', 'tov': '3', 'orb': '2', 'stl': '1', 'ft': '1', 'fg3a': '8', 'plus_minus': '-6', 'mp': '35:34', 'fta': '2', 'fg3': '3', 'fga': '20', 'ast': '5'}],
                         ['Russell Westbrook', {'blk': '1', 'drb': '12', 'fg': '10', 'pf': '5', 'opp': 'CHO', 'tov': '4', 'orb': '3', 'stl': '2', 'ft': '11', 'fg3a': '12', 'plus_minus': '-8', 'mp': '33:48', 'fta': '13', 'fg3': '2', 'fga': '31', 'ast': '8'}],
                         ['Andre Roberson', {'blk': '0', 'drb': '1', 'fg': '1', 'pf': '3', 'opp': 'CHO', 'tov': '1', 'orb': '1', 'stl': '0', 'ft': '0', 'fg3a': '1', 'plus_minus': '-10', 'mp': '29:59', 'fta': '0', 'fg3': '0', 'fga': '3', 'ast': '1'}],
                         ['Domantas Sabonis', {'blk': '0', 'drb': '2', 'fg': '1', 'pf': '3', 'opp': 'CHO', 'tov': '0', 'orb': '1', 'stl': '0', 'ft': '0', 'fg3a': '0', 'plus_minus': '-8', 'mp': '17:11', 'fta': '0', 'fg3': '0', 'fga': '4', 'ast': '0'}],
                         ['Jerami Grant', {'blk': '1', 'drb': '3', 'fg': '1', 'pf': '0', 'opp': 'CHO', 'tov': '1', 'orb': '1', 'stl': '0', 'ft': '0', 'fg3a': '0', 'plus_minus': '-2', 'mp': '27:21', 'fta': '0', 'fg3': '0', 'fga': '2', 'ast': '0'}],
                         ['Alex Abrines', {'blk': '0', 'drb': '1', 'fg': '2', 'pf': '4', 'opp': 'CHO', 'tov': '0', 'orb': '0', 'stl': '2', 'ft': '0', 'fg3a': '5', 'plus_minus': '0', 'mp': '21:15', 'fta': '0', 'fg3': '2', 'fga': '6', 'ast': '0'}],
                         ['Enes Kanter', {'blk': '0', 'drb': '6', 'fg': '8', 'pf': '3', 'opp': 'CHO', 'tov': '1', 'orb': '2', 'stl': '0', 'ft': '5', 'fg3a': '2', 'plus_minus': '-4', 'mp': '19:30', 'fta': '6', 'fg3': '1', 'fga': '13', 'ast': '0'}],
                         ['Semaj Christon', {'blk': '0', 'drb': '3', 'fg': '2', 'pf': '2', 'opp': 'CHO', 'tov': '2', 'orb': '0', 'stl': '0', 'ft': '0', 'fg3a': '0', 'plus_minus': '-4', 'mp': '14:39', 'fta': '0', 'fg3': '0', 'fga': '3', 'ast': '5'}],
                         ['Anthony Morrow', {'blk': '0', 'drb': '0', 'fg': '2', 'pf': '1', 'opp': 'CHO', 'tov': '0', 'orb': '0', 'stl': '0', 'ft': '0', 'fg3a': '2', 'plus_minus': '-5', 'mp': '4:14', 'fta': '0', 'fg3': '1', 'fga': '4', 'ast': '0'}],
                         None],
                    'homeTeamData':
                        {'blk': '3', 'drb': '37', 'fg': '42', 'pf': '31', 'opp': 'CHO', 'orb': '14', 'stl': '6', 'ft': '19', 'fg3a': '30', 'tov': '14', 'fta': '23', 'fg3': '9', 'fga': '96', 'ast': '22'},
                    'awayTeamData':
                        {'fga': '80', 'fta': '49', 'tov': '11', 'stl': '8', 'fg3a': '24', 'opp': 'OKC', 'drb': '33','orb': '10', 'ast': '25', 'ft': '40', 'fg3': '9', 'fg': '37', 'pf': '21', 'blk': '10'}
                   }]


    def testParse(self):
        SingleGameDataScraper(link).generate()


if __name__ == '__main__':
    unittest.main()