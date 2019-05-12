import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import csv
from multiprocessing import Pool

url = "https://hh.ru/search/vacancy?text=Python&area=1"


class Parser: #Create class of methods

    def __init__(self):
        self.headers = {"User-Agent":UserAgent().chrome}

    def get_html(self, url):

        with requests.session() as s:

            page = s.get(url, headers=self.headers).content
            return page

    def get_all_links(self, page): #get all pages
        soup = bs(page, "lxml")

        num = soup.find_all("a", attrs={"class":"bloko-button HH-Pager-Control"})[-1].text

        return int(num)



    def get_info(self, page):
        soup = bs(page, "lxml")

        names = soup.find_all("a", attrs={"data-qa":"vacancy-serp__vacancy-title"})
        citys = soup.find_all("span", attrs={"data-qa":"vacancy-serp__vacancy-address"})
        prices = soup.find_all("div", attrs={"class":"vacancy-serp-item__compensation"})
        urls = soup.find_all("div", attrs={"class":"resume-search-item__name"})

        for d in range(len(names)):

            try:
                name = names[d].text
                print(name)
            except:
                name = ""

            try:
                city = citys[d].text
            except:
                city = ""

            try:
                price = prices[d].text

            except:
                price = ""

            try:
                url = urls[d].find("a")["href"]

            except:
                url = ""

            data = {"name" : name, "city" : city, "price" : price, "url" : url}

            self.write_csv(data)

    def write_csv(self, data):

        with open("orders.csv","a") as f:
            writer = csv.writer(f)

            writer.writerow( (data["name"], data["city"], data["price"], data["url"] ) )


def make_all(url):
    bot = Parser()
    page = bot.get_html(url)
    bot.get_info(page)


def main(url):
    bot = Parser()
    html = bot.get_html(url)
    links =[url+"&page={0}".format(x) for x in range(bot.get_all_links(html))]
    for link in links:
        print(link)

    with Pool(20) as p:
        p.map(make_all, links)

if __name__=="__main__":
    main(url)
