import urllib.request as url
class HTMLParser(object):

    @classmethod
    def parse(cls, link):
        response = str(url.urlopen(link).read())
        body = HTMLParser().HTMLBody(response)
        return HTMLParser().RawtoCleanHTML(body)

    @classmethod
    def RawtoCleanHTML(cls, text):
        remove_list= ["\\n", "  ", "\\r", "\\t"]
        new_text= text
        for i in remove_list:
            new_text = new_text.replace(i, "")
        new_text = HTMLParser().removeComments(new_text)
        new_text = HTMLParser().removeScripts(new_text)
        return new_text

    @staticmethod
    def HTMLBody(HTML):
        start = HTML.find("<body")
        end = HTML.rfind("</body>")
        return HTML[start: (end + 7)]

    @staticmethod
    def removeScripts(HTML):
        while HTML.find('<script') != -1:
            start = HTML.find('<script')
            end = HTML.find("</script>") +  9
            script = HTML[start:end]
            HTML = HTML.replace(script, '')
        return HTML

    @staticmethod
    def removeComments(HTML):
        while HTML.find('<!') != -1:

            start = HTML.find('<!')
            end = HTML.find("-->") + 3
            comment = HTML[start: end]
            HTML = HTML.replace(comment, '')
        return HTML
