from html.parser import HTMLParser
from urllib import parse

class LinkParser(HTMLParser ):


    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()


    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for(k, v) in attrs:
                if k == 'href':
                    url = parse.urljoin(self.base_url, v)
                    self.links.add(url)


    def error(selfself, message):
        pass
