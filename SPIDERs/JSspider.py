# -*-coding=utf-8-*-
__author__ = 'LiuJingYuan'
import random
import urllib
import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from CONGs.config import USER_AGENTS, service_args, URLS

__author__ = 'LiuJingYuan'

class jsspider():
    def __init__(self):
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap["phantomjs.page.settings.loadImages"] = False
        self.dcap["phantomjs.page.settings.resourceTimeout"] = 5000
        self.re_userAgent()
        self.driver = webdriver.PhantomJS(
                desired_capabilities=self.dcap,
                service_args=service_args
            )

    def re_userAgent(self):
        self.dcap["phantomjs.page.settings.userAgent"] = random.choice(USER_AGENTS)
        return self.dcap["phantomjs.page.settings.userAgent"]

    def get_req(self,key):
        url = URLS[0].format(urllib.quote(key))
        # print url
        self.driver.get(url)
        time.sleep(5)
        gsurl = self.driver.find_element_by_xpath('//div[@class="search_right_item"]/div[1]/div[1]/a').get_attribute("href")
        print gsurl
        self.driver.get(gsurl)
        time.sleep(5)
        # print len(self.driver.page_source),self.driver.page_source
        return self.driver.page_source,gsurl

    def close(self):
        self.driver.close()

if __name__ == '__main__':
    pass