from HTMLParser import *
import unittest

LINK = "http://www.math.uah.edu/stat/Search.html"

EXPECTED_RESULT = '<body class="ancillary"><header><h2 class="ancillary">Search Random</h2></header>'\
'<div class="search"><gcse:search linkTarget="main"></gcse:search></div><footer><ol class="map">'\
'<li class="parent"><a href="index.html" class="main">Random</a></li><li class="child">Search</li>'\
        '</ol></footer></body>'




class HTMLParserTest(unittest.TestCase):
    def setUp(self):
        self.HTMLParser = HTMLParser().parse(LINK)
        self.result = EXPECTED_RESULT

    def testParse(self):
        self.assertEqual(self.result, self.HTMLParser, "Testing HTMLParser.parse()")

if __name__ == '__main__':
    unittest.main()