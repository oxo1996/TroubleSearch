from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import requests
from selenium.common.exceptions import NoSuchElementException

class CrawlKo2Eng(crawlable):
    def __init__(self):
        self.link = "http://kcia.or.kr/cid/search/ingd_list.php?skind=ALL&sword="
        self.driver = webdriver.Chrome("chromedriver")

    def _readFile(self, path):
        with open(path) as json_file:
            json_data = json.load(json_file)
        return json_data

    def _crawling(self):
        items = self._readFile("items.json")
        eng_dict = self._readFile("ingrKo2Eng.json")
        
        self.driver.implicitly_wait(10)
        self.driver.get(self.link)

        i = 0
        for name in items.keys():
            ingrList = items[name]["ingredients"]
            #print(ingrList)
            for ingr in ingrList:
                if ingr in eng_dict.keys():
                    print(ingr + "is exist")
                    continue
                #print(ingr)
                inputName = '\"' + ingr + '\"'
                searchBox = self.driver.find_element_by_xpath("//*[@class='input_search']")
                searchBox.clear()
                self.driver.implicitly_wait(5)
                searchBox.send_keys(inputName)
                searchBox.submit()

                try:
                    engName = self.driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/table/tbody[2]/tr/td[3]/a")
                    #eng_dict[ingr] = engName.text      에러나면 이걸로
                    eng_dict[ingr] = engName.text.replace('/', '&') # '/' 때문에 에러나서 수정함. 에러 나면 위
                    print(eng_dict[ingr])
                except NoSuchElementException as e:
                    print("not found ", ingr)
                    continue

            with open('ingrKo2Eng.json', 'w', encoding='utf-8') as make_file:
                json.dump(eng_dict, make_file, indent="\t")

    def getData(self):
        data = self._crawling()
        return data