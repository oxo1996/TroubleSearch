from crawlable import crawlable
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
import json
import urllib.request
import re


class Ewg(crawlable):
    def __init__(self):
        self._link = "https://www.ewg.org/skindeep/ingredient/702002/DIISOSTEARYL_MALATE/"
        self._driver = webdriver.Chrome("chromedriver")

    def _remove_htmltag(self, readData):
        text = re.sub('<.+?>', '', readData, 0).strip()
        return text

    def _read_file(self, path):
        with open(path) as json_file:
            json_data = json.load(json_file)
        return json_data

    def _get_image(self, img_name):
        _opener = urllib.request.build_opener()
        _opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(_opener)

        _image_link = self._driver.find_element_by_xpath("//*[@id='chemical']/div/img").get_attribute("src")
        urllib.request.urlretrieve(_image_link, "./ewgrank/" + img_name + ".png")

    def _get_desc(self):
        _curr_html = self._driver.page_source
        _soup = BeautifulSoup(_curr_html, "html.parser")

        for section in _soup.select("#chemical"):
            section.decompose()
        for section in _soup.select("section.see-all-chemical"):
            section.decompose()
        for section in _soup.select("section.gauges.ingredients.grid"):
            section.decompose()
        for section in _soup.select("section.block"):
            section.decompose()
        for section in _soup.select("section.product-about.text-block"):
            section.decompose()
        for section in _soup.select("main > section"):
            if "Products with this Ingredient" in section.text:
                section.decompose()
            for head in _soup.select("main > section > div > table > thead > tr"):
                head.decompose()
            for reference in _soup.select("main > section > div > table > tbody > tr > td:nth-child(2)"):
                reference.decompose()

        desc = _soup.select("body > div.content > div > main")
        desc = self._remove_htmltag(str(desc))
        desc = re.sub('[\n]+', '\n', desc)
        return desc.strip()

    def _crawling(self):
        ''' 구버전.
            현재 ewg 사이트 개편으로 정상적으로 동작하지 않음.
        '''
        _category = "ewg"
        _ingr_ko2eng = self._read_file("ingrKo2Eng.json")
        ingr_desc = self._read_file("ingrDesc.json")
        self._driver.implicitly_wait(10)
        self._driver.get(self._link)

        _adbox = self._driver.find_element_by_xpath("//div[@class='sidebar-iframe-close']")
        _adbox.click()

        for ko_name in _ingr_ko2eng.keys():
            eng_name = _ingr_ko2eng[ko_name]
            if eng_name in ingr_desc[_category].keys():
                continue
            _searchbox = self._driver.find_element_by_xpath("//*[@id='s']")
            self._driver.implicitly_wait(5)
            _searchbox.send_keys(eng_name)
            _searchbox.submit()
            try:
                self._get_image(eng_name)
                _ingr_btn = self._driver.find_element_by_xpath("//*[@align='left']/a")
                _ingr_btn.send_keys('\n')
                print(eng_name)
                try:
                    ingr_desc[_category][eng_name] = self._get_desc()
                    with open('ingrDesc.json', 'w', encoding='utf-8') as make_file:
                        json.dump(ingr_desc, make_file, indent="\t")
                except AttributeError:
                    print("not found in " + _category)
            except NoSuchElementException as e:
                print("no information " + eng_name)
                continue

        return ingr_desc

    def _crawling_with_daum(self):
        '''다음에서 크롤링한 성분을 ewg에서 크롤링함.'''
        ingr_desc = self._read_file("ingrDesc.json")
        self._driver.implicitly_wait(10)
        self._driver.get(self._link)

        _adbox = self._driver.find_element_by_xpath("//*[@id='yeaClose']")
        _adbox.click()

        ischeck = False
        for ko_name in ingr_desc.keys():
            if ko_name != "오쿠메수지추출물" and ischeck != True:
                '''임시용.
                    자꾸 끊겨서 시작지점을 만듬.'''
                print("pass")
                continue
            else:
                ischeck = True

            print(ko_name)
            eng_name = ingr_desc[ko_name]["engName"]
            eng_name = eng_name.replace('/', '&')
            ingr_desc[ko_name]["engName"] = eng_name  # 이름 중간에 '/'를 '&'로 바꾸고 다시 저장

            if "engDesc" in ingr_desc[ko_name].keys():
                print("already process")
                continue
            _searchbox = self._driver.find_element_by_xpath("//*[@id='search']")
            self._driver.implicitly_wait(5)

            _searchbox.clear()
            _searchbox.send_keys(eng_name)
            _search_btn = self._driver.find_element_by_xpath("/html/body/div/header/div/div/section/form/button")
            _search_btn.send_keys(Keys.ENTER)

            _curr_html = self._driver.page_source
            _soup = BeautifulSoup(_curr_html, "html.parser")
            _search_result_list = _soup.select(
                "body > div.content > div > main > section.browse-search-header > span > ul > li > a")

            for search_result in _search_result_list:
                link = search_result.get("href")
                if "ingredient" in link:
                    self._driver.get(link)
            try:
                _ingr_btn = self._driver.find_element_by_xpath("/html/body/div/div/main/section/div[1]/p/a")
                _ingr_btn.click()
                self._get_image(ingr_desc[ko_name]["engName"])
                # try:
                ingr_desc[ko_name]["engDesc"] = self._get_desc()
                with open('ingrDesc.json', 'w', encoding='utf-8') as make_file:
                    json.dump(ingr_desc, make_file, indent="\t")
                # except AttributeError:
                #     print("not found in " + _category)
            except (NoSuchElementException, ElementNotInteractableException) as e:
                print(e)
                print("no information " + eng_name)
                continue
        return ingr_desc

    def get_data(self):
        # data = self._crawling()
        data = self._crawling_with_daum()
        print("complete")
        return data
