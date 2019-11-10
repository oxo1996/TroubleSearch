from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json
import re

class CrawlDaumIngr(crawlable):
    def __init__(self):
        self.link = "https://100.daum.net/book/542/list"
        self.defaultLink = "https://100.daum.net/"
        self.driver = webdriver.Chrome("chromedriver")

    def _removeHtmlTag(self, readData):
        text = re.sub('<.+?>', '', readData, 0).strip()
        return text

    def _getIngrLink(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        ingrList = soup.select("#mArticle > div > ul > li > div > strong > a")
        #mArticle > div > ul > li:nth-child(2) > div > strong
        #ingrList = self.driver.find_element_by_xpath("//*[@id='mArticle']/div/ul")

        ingrLinks = []
        for link in ingrList:
            ingrLinks.append(self.defaultLink + link.get("href"))
        
        return ingrLinks

    def _getName(self, selectorPath : str):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        name = soup.select(selectorPath)
        print(name[0].text.strip())
        return name[0].text.strip()

    def _getDesc(self):
        resultDesc = ""
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        descList = soup.select("div.info_cont.info_details > div > p")

        for desc in descList:
            desc = re.sub("각주1\)", '', desc.text)
            resultDesc += "\n" + self._removeHtmlTag(desc)
        return resultDesc.strip()

    def _getEwgRank(self, readData : str):
        regex = re.compile(r'\d등급')
        match = regex.search(readData)
        try:
            rawrank = match.group()
            rank = re.sub('등급', '', rawrank).strip()
        except AttributeError as e:
            print(e)
            print("ewg 등급이 없습니다.")
            rank = 0
        return int(rank)

    def _readFile(self, path):
        try:
            print("read file")
            with open(path) as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError as e:
            print(e)
            json_data = {}
        return json_data

    def _crawling(self):
        ingrDesc = self._readFile("daumIngrDesc.json")
        self.driver.implicitly_wait(10)
        self.driver.get(self.link)
        
        page = 488    # 시작 페이지 설정
        while True:
            print(page)
            ingrLinks = self._getIngrLink()
            if len(ingrLinks) <= 0:
                print("end")
                break

            for link in ingrLinks:
                self.driver.get(link)
                koName = self._getName("div.info_cont.info_tit > div > div > div.area_tit > h3")
                if koName in ingrDesc.keys():
                    print("exist ingredients")
                    continue
                engName = self._getName("div.info_cont.info_tit > div > div > div.area_tit > strong")
                desc = self._getDesc()
                rank = self._getEwgRank(desc)
                ingrDesc[koName] = {}
                ingrDesc[koName]["engName"] = engName
                ingrDesc[koName]["ewgRank"] = rank
                ingrDesc[koName]["koDesc"] = desc    
                with open('daumIngrDesc.json', 'w', encoding='utf-8') as make_file:
                    json.dump(ingrDesc, make_file, indent="\t")
            print("now num of keys: ", len(ingrDesc))       

            page += 1
            nextPageLink = self.defaultLink + "book/542/list?sort=vcnt&index=&page=" + str(page)
            self.driver.implicitly_wait(10)
            self.driver.get(nextPageLink)
        
        return ingrDesc

    def getData(self):
        ingr = self._crawling()
        return ingr