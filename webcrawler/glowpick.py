from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import urllib.request
import json
import time


class Glowpick(crawlable):
    def __init__(self, path, ctg):
        self.link = path
        self.category = ctg
        self.driver = webdriver.Chrome("chromedriver")

    def _readFile(self, path):
        try:
            print("read file")
            with open(path) as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError as e:
            print(e)
            json_data = {}
        return json_data

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
        productList = soup.select("section.section-list > ul > li > meta:nth-child(2)")
        productLinks = []
        for link in productList:
            productLinks.append(link.get("content"))

        return productLinks

    def _getBrand(self):
        brand = self.driver.find_element_by_xpath("//*[@id='gp-product-detail']/div/ul[1]/li[2]/div/section[1]/p").text
        brand = re.sub(r'\([^)]*\)', '', brand)
        return brand.strip()

    def _getImage(self, imgName):
        imageLink = self.driver.find_element_by_xpath(
            "//*[@id='gp-product-detail']/div/ul[1]/li[1]/div/section/figure/div/img").get_attribute("src")
        urllib.request.urlretrieve(imageLink, "./img/" + imgName + ".png")
        return imageLink

    def _getIngredients(self):
        ingredients = []
        ingrBtn = self.driver.find_elements_by_xpath(
            "//*[@id='gp-product-detail']/div/ul/li/div/section/div/div/button")
        try:
            ingrBtn[0].click()
        except IndexError as e:
            return -1

        htmlTemp = self.driver.page_source
        soup = BeautifulSoup(htmlTemp, "html.parser")
        ingrList = soup.select("#gp-popup > div > section.side-info.ingredient > div.list-ingredient > ul > li > \
        div.list-ingredient__item__row.list-ingredient__item__text > p.list-ingredient__item__text-korean")
        for ingr in ingrList:
            ig = ingr.text.strip()
            splitIngr = ig.split(';')
            for elem in splitIngr:
                ingredients.append(elem.strip())

        closeBtn = self.driver.find_element_by_xpath("//*[@id='gp-popup-bg']/button")
        closeBtn.click()
        return ingredients

    def _getEachRankReview(self, reviews, pushedBtn, pushingBtn, rank):
        filterBtn = self.driver.find_element_by_xpath(
            "//*[@id='gp-product-detail']/div/ul/li/section/div/section/div/div/button")
        if pushedBtn != -1:
            pushedBtn.click()
        pushingBtn.click()
        filterBtn.click()

        body = self.driver.find_element_by_tag_name('body')
        body.click()

        numOfPagedowns = 10
        while numOfPagedowns:
            body.send_keys(Keys.END)
            time.sleep(0.3)
            numOfPagedowns -= 1

        htmlTemp = self.driver.page_source
        soup = BeautifulSoup(htmlTemp, "html.parser")
        reviewList = soup.select(
            "#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section > ul > li > div > p")
        for review in reviewList:
            reviews.append((rank, review.text.strip()))

    def _getReview(self):
        reviews = []
        sosoBtn = self.driver.find_element_by_xpath(
            "//*[@id='gp-product-detail']/div/ul/li/section/div/section/div/form/fieldset[4]/ul/li[4]")
        notgoodBtn = self.driver.find_element_by_xpath(
            "//*[@id='gp-product-detail']/div/ul/li/section/div/section/div/form/fieldset[4]/ul/li[5]")
        worstBtn = self.driver.find_element_by_xpath(
            "//*[@id='gp-product-detail']/div/ul/li/section/div/section/div/form/fieldset[4]/ul/li[6]")

        self._getEachRankReview(reviews, -1, sosoBtn, 3)
        self._getEachRankReview(reviews, sosoBtn, notgoodBtn, 2)
        self._getEachRankReview(reviews, notgoodBtn, worstBtn, 1)
        return reviews

    def _crawling(self):
        items = self._readFile("items.json")
        self.driver.implicitly_wait(10)
        self.driver.get(self.link)

        body = self.driver.find_element_by_tag_name('body')
        body.click()

        numOfPagedowns = 10
        while numOfPagedowns:
            body.send_keys(Keys.END)
            time.sleep(0.3)
            numOfPagedowns -= 1

        productLinks = self._getProductLink()
        for link in productLinks:
            self.driver.get(link)
            pname = self.driver.find_element_by_xpath(
                "//*[@id='gp-product-detail']/div/ul/li/div/section/h1/span").text.strip()
            pname = pname.replace('/', '&')
            print(pname)
            if pname in items.keys():
                print("exist item")
                continue

            ingredients = self._getIngredients()
            if ingredients == -1:
                print("not exist ingredients")
                continue

            items[pname] = {}
            items[pname]["categories"] = self.category
            items[pname]["brand"] = self._getBrand()
            items[pname]["imageLink"] = self._getImage(items[pname]["brand"] + "_" + pname)
            items[pname]["ingredients"] = ingredients
            items[pname]["reviews"] = self._getReview()

            with open('items.json', 'w', encoding='utf-8') as make_file:
                json.dump(items, make_file, indent="\t")

    def get_data(self):
        product = self._crawling()
        return product
