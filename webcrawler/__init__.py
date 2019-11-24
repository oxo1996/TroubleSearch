from webcrawler import webcrawler
from crawlable import crawlable
from amore import Amore
from ko2eng import Ko2Eng
from ewg import Ewg
from daumIngr import DaumIngr
from glowpick import Glowpick


def crawl_amore():
    allCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001?upperMenuId=CTG001&categoryType=category"
    skinCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002001?upperMenuId=CTG001002001&categoryType=category"
    lotionCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002002?upperMenuId=CTG001002002&categoryType=category"
    essenceCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002003?upperMenuId=CTG001002003&categoryType=category"
    creamCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002004?upperMenuId=CTG001002004&categoryType=category"
    mistCategory = "https://www.amorepacificmall.com/kr/ko/display/category/CTG001002006?upperMenuId=CTG001002006&categoryType=category"

    execList = [(creamCategory, "cream"), (mistCategory, "mist"), (skinCategory, "toner"), (lotionCategory, "lotion"),
                (essenceCategory, "essence")]
    # execList = [(lotionCategory, "lotion"), (essenceCategory, "essence"), (creamCategory, "cream"), (mistCategory, "mist")]
    for exc in execList:
        amore = Amore(exc[0], exc[1])
        data = webcrawler.crawlData(amore)

    print("fully success")


def crawl_ko2eng():
    ko2eng = Ko2Eng()
    data = webcrawler.crawlData(ko2eng)


def crawl_ewg():
    ewg = Ewg()
    data = webcrawler.crawlData(ewg)


def crawl_glowpick():
    skinCategory = "https://www.glowpick.com/beauty/ranking?id=2"
    lotionCategory = "https://www.glowpick.com/beauty/ranking?id=3"
    tonerCategory = "https://www.glowpick.com/beauty/ranking?id=210"
    essenceCategory = "https://www.glowpick.com/beauty/ranking?id=4"
    creamCategory = "https://www.glowpick.com/beauty/ranking?id=5"
    mistCategory = "https://www.glowpick.com/beauty/ranking?id=1"

    # execList = [(skinCategory, "skin"), (lotionCategory, "lotion"), (tonerCategory, "toner"), (essenceCategory, "essence"), \
    # (creamCategory, "cream"), (mistCategory, "mist")]
    execList = [(mistCategory, "mist")]

    for exc in execList:
        glowpick = Glowpick(exc[0], exc[1])
        data = webcrawler.crawl_data(glowpick)

    print("fully success")


if __name__ == '__main__':
    # ewg = Ewg()
    # webcrawler.crawl_data(ewg)
    # crawl_glowpick()
    ko2eng = Ko2Eng()
    ko2eng.get_data()
