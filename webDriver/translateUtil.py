#coding=utf-8

from selenium import webdriver
import time
import os

browser = webdriver.Chrome('WebUI\chromedriver.exe')

class Translator:
    def __init__(self):
        self.browser = webdriver.Chrome('WebUI\chromedriver.exe')

    def read_file(self, file_path):
        if file_path and os.path.isfile(file_path):
            file = open(file_path, 'r')

        else:
            raise Exception("input is not a file, please input a valid file")

    def translate_file(self, file_path):
        browser.get("https://translate.google.cn")  # Load page

    def translate_words(self, word):
        browser.get("https://translate.google.cn")  # Load page
        browser.find_element_by_xpath('//*[@id="source"]').send_keys("word")
        time.sleep(5)
        output = browser.find_element_by_xpath('//*[@id="gt-res-dir-ctr"]')
        return output.text

if __name__=='__main__':
    translator = Translator()
    result = translator.translate_words(u"幫我搜索一個關於 <topic> 的話題")
    print (result)


