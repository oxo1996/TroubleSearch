from translator import translator
from papagonmt import papagonmt

if __name__ == '__main__':
    nmt = papagonmt()
    translatedStr = nmt.translate( \
        "제품 잘 받았습니다. 배송이 빠르네요. 포장도 꼼꼼하게 해 주셨어요. \
        시향을 해보지 않고 바로 구매했는데 잘 산 것 같아요. \
        제가 좋아하는 향이라 다행입니다. 양도 많아서 오랫동안 사용할 수 있을 것 같습니다. \
        잘 쓸게요.", "ko", "en")
    print(translatedStr)
