from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json
import urllib.request
import re

class CrawlEwg(crawlable):
    def __init__(self):
        self.link = "https://www.ewg.org/skindeep/ingredient/702002/DIISOSTEARYL_MALATE/"
        self.driver = webdriver.Chrome("chromedriver")

    def _removeHtmlTag(self, readData):
        text = re.sub('<.+?>', '', readData, 0).strip()
        return text

    def _readFile(self, path):
        with open(path) as json_file:
            json_data = json.load(json_file)
        return json_data

    def _getImage(self, imgName):
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        
        imageLink = self.driver.find_element_by_xpath("//*[@id='prod_cntr_score']/div[1]/a/img").get_attribute("src")
        urllib.request.urlretrieve(imageLink, "./ewgrank/" + imgName + ".png")

    def _getDesc(self):
        htmlTemp = self.driver.page_source
        soup = BeautifulSoup(htmlTemp, "html.parser")    
        try:    
            for div in soup.find_all("div", {"class":"product_small_font"}):
                div.decompose()
            soup.find("div", id="Products").decompose()
            desc = soup.select("div.rightside_content2012")
            desc = self._removeHtmlTag(str(desc))
            print(desc)
        except AttributeError as e:
            print("no information description")
            

    def _crawling(self):
        ingrEwg = {}
        ingrKo2Eng = self._readFile("ingrKo2Eng.json")
        self.driver.implicitly_wait(10)
        self.driver.get(self.link)

        adbox = self.driver.find_element_by_xpath("//div[@class='sidebar-iframe-close']")
        #adbox.send_keys('\n')
        adbox.click()

        for koName in ingrKo2Eng.keys():
            engName = ingrKo2Eng[koName]
            searchBox = self.driver.find_element_by_xpath("//*[@id='s']")
            #searchBox.clear()
            
            self.driver.implicitly_wait(5)
            searchBox.send_keys(engName)
            searchBox.submit()

            try:
                self._getImage(engName)            
                ingrBtn = self.driver.find_element_by_xpath("//*[@align='left']/a")
                ingrBtn.send_keys('\n')
                print(engName)
                self._getDesc()
            except NoSuchElementException as e:
                print("no information " + engName)
                continue

        return ingrEwg

    def getData(self):
        data = self._crawling()
        return data