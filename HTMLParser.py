import urllib.request as url
class HTMLParser(object):

    @classmethod
    def parse(cls, link):
        response = url.urlopen(link)
        html = self.RawtoCleanHTML(str(response.read()))
        return html[html.find("<body"): html.find("</body>")]

    def RawtoCleanHTML(self, text):
        remove_list= ["\\n", "  ", "\\r", "\\t"]
        new_text= text
        for i in remove_list:
            new_text = new_text.replace(i, "")
        return new_text