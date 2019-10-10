from webcrawler import webcrawler
from CrawlAmore import CrawlAmore
from CrawlKo2Eng import CrawlKo2Eng
from CrawlEwg import CrawlEwg

def crawlAmore():
    allCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001?upperMenuId=CTG001&categoryType=category"
    skinCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002001?upperMenuId=CTG001002001&categoryType=category"
    lotionCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002002?upperMenuId=CTG001002002&categoryType=category"
    essenceCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002003?upperMenuId=CTG001002003&categoryType=category"
    creamCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002004?upperMenuId=CTG001002004&categoryType=category"
    mistCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002006?upperMenuId=CTG001002006&categoryType=category"

    execList = [(creamCategory, "cream"), (mistCategory, "mist"), (skinCategory, "toner"), (lotionCategory, "lotion"), (essenceCategory, "essence")]
    #execList = [(lotionCategory, "lotion"), (essenceCategory, "essence"), (creamCategory, "cream"), (mistCategory, "mist")]
    for exc in execList:
        amore = CrawlAmore(exc[0], exc[1])
        data = webcrawler.crawlData(amore)

    print("fully success")

def crawlKo2Eng():
    ko2eng = CrawlKo2Eng()
    data = webcrawler.crawlData(ko2eng)

def crawlEwg():
    ewg = CrawlEwg()
    data = webcrawler.crawlData(ewg)

if __name__ == '__main__':
    crawlEwg()
    # crawlKo2Eng()
    # Ko2Eng = CrawlKo2Eng()
    # data = webcrawler.crawlData(Ko2Eng)