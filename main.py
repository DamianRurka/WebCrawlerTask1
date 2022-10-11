from html.parser import HTMLParser as HPr
from urllib import parse
from urllib.request import urlopen

class LinkParser(HPr):

    def url_reader(self, tag, attrs):
        if tag == 'a':
            for(k, v) in attrs:
                if k == 'href':
                    nUrl = parse.urljoin(self.bUrl, v)
                    self.links = self.links + [nUrl]

    def get_link(self, url):
        self.links = []
        self.bUrl = url
        response = urlopen(url)
        print("next?")
        if response.getheader('Content-Type')=='text/html':
            print("yes")
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            print("false")
            return "",[]

def spider_program(url, word,maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]

                                    #TODO:save data to csv
        parser = LinkParser()
        data, links = parser.get_link(url)
        if data.find(word) >-1:
            foundWord = True
        pagesToVisit = pagesToVisit + links
        print(numberVisited)

    if foundWord:
        print("secure detected,spider program: OFF ")

start = spider_program("https://www.google.com/", "secure", 20)

