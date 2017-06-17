#coding=utf-8
from selenium import webdriver
import time


def login_by_erp(driver, uid, passwd):

    driver.get("http://erp.jd.com")
    driver.find_element_by_xpath(".//*[@id='username']").send_keys(uid)
    time.sleep(0.2)
    driver.find_element_by_xpath(".//*[@id='password']").send_keys(passwd)
    time.sleep(0.2)
    driver.find_element_by_xpath(".//*[@class='formsubmit_btn']").click()


def open(driver):

    driver.get("http://buser.ka.jd.com")
    time.sleep(5)
    driver.find_element_by_xpath(".//*[@id='j_nav_9']").click()
    driver.find_element_by_xpath(".//*[@id='j_sub_nav_92']/span").click()
    driver.find_element_by_xpath(".//*[@id='nameLike_search']").send_keys(u"京东价测试")
    driver.find_element_by_xpath(".//*[@onclick='queryList();']").click()

if __name__ == "__main__":
    driver = webdriver.Chrome('D:\Tools\DevTools\WebUI\chromedriver.exe')
    #driver = webdriver.Chrome()
    login_by_erp(driver,"***","****")
    #open(driver)