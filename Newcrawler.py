import requests
from bs4 import BeautifulSoup


class WebCrawler:
    url = ""

    def __init__(self,new_url):
        WebCrawler.url = new_url
        self.get_links()

    def get_links(self, new_url):
        self.url = "https://www.youtube.com/"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.pages_number = -1
        self.link_title_dict = dict()
        self.link_views_dict = dict()
        self.id_link = dict()
        self.IDX = 0
        for link in self.soup.find_all('a', href=True):
            get_link = (f"{link.get('href')}")
            get_title = (f"{link.string}")
            self.views_pages_number = 0

            if get_link == '/None' or \
                    get_link == "/" or\
                    get_link == "/new" or \
                    get_link == "/t/terms" or \
                    get_link == "/t/privacy" or\
                    get_link == '/t/contact_us/':
                continue
            if get_link in self.link_title_dict:
                self.views_pages_number = self.link_views_dict.get(get_link)
                new_views_pages_number = self.views_pages_number + 1
                self.link_views_dict = {get_link: new_views_pages_number}
                continue
            else:
                for k, v in self.link_title_dict.items():
                    print("{}: {}".format(k, v))
                self.link_title_dict = {get_link: get_title}
                self.pages_number += 1                #TODO:liczba podstron na stronie
                self.link_views_dict = {get_link: 1}  #TODO: number of page views
                self.id_link = {self.IDX: get_link}

        new_url_for_spider = self.id_link.get(self.IDX)
        if new_url_for_spider != self.url:
    #         url = new_url_for_spider  ZMIENNA GLOBALNA!!!
    # get_links(url)



start = WebCrawler()