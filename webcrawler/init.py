from webcrawler import webcrawler
from CrawlAmore import CrawlAmore
from CrawlKo2Eng import CrawlKo2Eng

if __name__ == '__main__':
    all_category = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001?upperMenuId=CTG001&categoryType=category"
    skin_category = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002001?upperMenuId=CTG001002001&categoryType=category"
    amore = CrawlAmore(skin_category)
    data = webcrawler.crawlData(amore)
    # Ko2Eng = CrawlKo2Eng()
    # data = webcrawler.crawlData(Ko2Eng)