from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import urllib.request
import json
import time

class CrawlAmore(crawlable):
    def __init__(self, path, ctg):
        self.mall_link = "https://www.amorepacificmall.com"
        self.mall_category = path
        self.category = ctg
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
        productLinks = soup.select("div.product_box > a")

        links = {}
        for link in productLinks:
            name = self._cleanText(link.get("ap-click-data"))
            links[name] = self.mall_link + link.get("href")
        return links

    def _getBrand(self):
        brand = self.driver.find_element_by_xpath("//div[@class='product_brand']/a")
        return brand.text

    def _getImage(self, imgName):
        imageLink = self.driver.find_element_by_xpath("//li[@class='ix-list-item']/img").get_attribute("src")
        urllib.request.urlretrieve(imageLink, "./img/" + imgName + ".png")
        return imageLink

    def _getIngredients(self):    
        ingredients = []     
        ingrBtn = self.driver.find_elements_by_xpath("//*[@class='btn_ingredient']")
        ingrBtn[0].send_keys(Keys.ENTER)
        htmlTemp = self.driver.page_source
        soup = BeautifulSoup(htmlTemp, "html.parser")
        ingr = soup.select("div > div> dl > dd > div > ul> li > p.txt")

        try:
            ingrStr = self._removeHtmlTag(str(ingr[0]))
            ingrStr = ingrStr.split(', ')
            for ig in ingrStr:
                ig = ig.replace("\n", '')   # 추가함(에러 나면 이거 볼 것)
                ingredients.append(ig.strip())
        except IndexError:
            print("not exist ingredients")

        closeBtn = self.driver.find_element_by_xpath("//*[@class='layer_btns']/a")
        closeBtn.send_keys('\n')

        return ingredients

    def _getReview(self):
        reviews = []
        reviewBtn = self.driver.find_element_by_xpath("//*[@id='ap_container']/div/div[3]/div[1]/ul/li[2]")        
        reviewBtn.click()

        for i in range(3, 0, -1):            
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
        self.driver.implicitly_wait(10)
        self.driver.get(self.mall_category)

        with open('C:\dev\django\djangoproject\webcrawler\items.json') as data_file:    
            items = json.load(data_file)
        #items = {}

        page = 1
        while True:
            print("running...", self.category, page)
            time.sleep(5)
            links = self._getProductLink()
            for pname in links.keys():        
                if pname in items.keys():
                    print("exist item")
                    continue 
                print(pname)
                link = links[pname]                
                self.driver.get(link)
                
                items[pname]= {}
                items[pname]["categories"] = self.category
                items[pname]["brand"] = self._getBrand()
                items[pname]["imageLink"] = self._getImage(items[pname]["brand"] + "_" + pname)
                items[pname]["ingredients"] = self._getIngredients()                
                items[pname]["reviews"] = self._getReview()                
            
            self.driver.get(self.mall_category)
            page += 1
            nextPageXpath = "//*[@data-page=\"" + str(page) + "\"]"
            try:
                self.driver.implicitly_wait(10)
                nextPageBtn = self.driver.find_element_by_xpath(nextPageXpath)
                nextPageBtn.send_keys('\n')
            except NoSuchElementException:
                print("finish")
                break
            with open('items.json', 'w', encoding='utf-8') as make_file:
                json.dump(items, make_file, indent="\t")
        return items

    def getData(self):
        ingr = self._crawling()
        return ingr