from translator import translator
from papagonmt import papagonmt

if __name__ == '__main__':
    nmt = papagonmt()
    print(nmt.translate("안녕하세요. 방금 밥 먹었어요.", "ko", "en"))