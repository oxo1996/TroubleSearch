from translator import translator
import os
import sys
import requests


class papagonmt(translator):
    def __init__(self):
        self.id = "UIScugDypFzyqlspTEuV"
        self.secret = "HXG21h7BD1"
        self.url = "https://openapi.naver.com/v1/papago/n2mt"

    def translate(self, inputStr: str, source: str, target: str):
        headers = {"X-Naver-Client-Id": self.id, "X-Naver-Client-Secret": self.secret}
        params = {"source": source, "target": target, "text": inputStr}
        response = requests.post(self.url, headers=headers, data=params)
        result = response.json()

        return result["message"]["result"]["translatedText"]
