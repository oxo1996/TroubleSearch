from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

class CrawlAmore(crawlable):
    def __init__(self):
        self.mall_link = "https://www.amorepacificmall.com"
        self.mall_category = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001?upperMenuId=CTG001&categoryType=category"
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
        self.driver.implicitly_wait(3)
        self.driver.get(self.mall_category)
        ingredients = {}

        page = 1
        while True:
            print(page)
            links = self._getProductLink()
            # nextPageBtn = self.driver.find_element_by_xpath("//*[@class='navi next']")
            # nextPageNumBtn = self._getPageNumBtn()

            # print(nextPageNumBtn)
            # nextPageNumBtn.send_keys('\n')


            # for name in links.keys():
            #     link = links[name]
            #     self.driver.get(link)
            #     print(link)
            #
            #     ingrBtn = self.driver.find_elements_by_xpath("//*[@class='btn_ingredient']")
            #     ingrBtn[0].send_keys(Keys.ENTER)
            #     htmlTemp = self.driver.page_source
            #     soup = BeautifulSoup(htmlTemp, "html.parser")
            #     ingr = soup.select("div > div> dl > dd > div > ul> li > p.txt")
            #     ingredients[name] = self._removeHtmlTag(str(ingr[0]))
            #     print("ingr: ", ingredients[name])

            page += 1
            nextPageXpath = "//*[@data-page=\"" + str(page) + "\"]"


            try:
                nextPageBtn = self.driver.find_element_by_xpath(nextPageXpath)
                nextPageBtn.send_keys('\n')
            except NoSuchElementException:
                print("finish")
                break

        return ingredients

    def getData(self):
        ingr = self._getIngredients()
        return ingr