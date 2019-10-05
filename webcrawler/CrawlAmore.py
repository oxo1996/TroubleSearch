from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json

class CrawlAmore(crawlable):
    def __init__(self, path):
        self.mall_link = "https://www.amorepacificmall.com"
        self.mall_category = path
        self.driver = webdriver.Chrome("chromedriver")

    def _cleanText(self, readData):
        text = re.sub('[/].*', '', readData)
        text = re.sub('\([^)]*\)', '', text)
        text = re.sub('\[[^)]*\]', '', text)
        text = text.lower()
        text = " ".join(text.split())
        text = text.strip()
        return text

    def _removeHtmlTag(self, readData):
        text = re.sub('<.+?>', '', readData, 0).strip()
        return text

    def _getProductLink(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        product_links = soup.select("div.product_box > a")

        links = {}
        for link in product_links:
            name = self._cleanText(link.get("ap-click-data"))
            links[name] = self.mall_link + link.get("href")
        return links

    def _getIngredients(self):    
        ingredients = []     
        ingrBtn = self.driver.find_elements_by_xpath("//*[@class='btn_ingredient']")
        ingrBtn[0].send_keys(Keys.ENTER)
        htmlTemp = self.driver.page_source
        soup = BeautifulSoup(htmlTemp, "html.parser")
        ingr = soup.select("div > div> dl > dd > div > ul> li > p.txt")

        ingrStr = self._removeHtmlTag(str(ingr[0]))
        ingrStr = ingrStr.split(',')
        for ig in ingrStr:
            ingredients.append(ig.strip())

        # ingredients[pname] = self._removeHtmlTag(str(ingr[0]))
        # print("ingr: ", ingredients[pname])

        closeBtn = self.driver.find_element_by_xpath("//*[@class='layer_btns']/a")
        closeBtn.send_keys('\n')

        return ingredients

    def _getReview(self):
        reviews = []
        reviewBtn = self.driver.find_element_by_xpath("//*[@id='ap_container']/div/div[3]/div[1]/ul/li[2]")        
        reviewBtn.click()

        for i in range(2, 0, -1):            
            reviewStat = "//*[@data-stat=\"" + str(i) + "\"]"
            reviewStatBtn = self.driver.find_element_by_xpath(reviewStat)
            reviewStatBtn.send_keys('\n')

            isMore = True
            while isMore:
                try:
                    listMore = "//*[@class='btn_list_more']/a"
                    listMoreBtn = self.driver.find_element_by_xpath(listMore)
                    self.driver.implicitly_wait(10)
                    listMoreBtn.send_keys('\n')
                except :
                    isMore = False
            
            htmlTemp = self.driver.page_source
            soup = BeautifulSoup(htmlTemp, "html.parser")
            review = soup.select("div.comment > div")
            for rv in review:
                reviews.append((i, self._removeHtmlTag(str(rv))))
            
        return reviews

    def _crawling(self):
        self.driver.implicitly_wait(3)
        self.driver.get(self.mall_category)
        items = {}

        page = 1
        while True:
            print("page: ", page)
            links = self._getProductLink()
            for pname in links.keys():
                link = links[pname]
                self.driver.get(link)

                items["name"] = pname
                items["ingredients"] = self._getIngredients()                
                items["reviews"] = self._getReview()
                print(pname)
            
            self.driver.get(self.mall_category)
            page += 1
            nextPageXpath = "//*[@data-page=\"" + str(page) + "\"]"
            try:
                nextPageBtn = self.driver.find_element_by_xpath(nextPageXpath)
                nextPageBtn.send_keys('\n')
            except NoSuchElementException:
                print("finish")
                break
            with open('items.json', 'w', encoding='utf-8') as make_file:
                json.dump(items, make_file, indent="\t")

    def getData(self):
        ingr = self._crawling()
        return ingr