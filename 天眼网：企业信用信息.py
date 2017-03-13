#encoding=utf8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib
import threading

class Mythread(threading.Thread):
    def __init__(self,func,args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        apply(self.func,self.args)


def tianyancha_spider(keyword,lock) :
    url = "http://www.tianyancha.com/search?key=%s&checkFrom=searchBox" % urllib.quote(keyword)
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.loadImages"] = False
    dcap["phantomjs.page.settings.resourceTimeout"] = 5000
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    service_args = [
    '--ignore-ssl-errors=true',
    '--cookies-file=test.cookies',
    '--disk-cache=true',
    '--local-to-remote-url-access=true',
    '--proxy=58.17.158.43:8998',
    # '--proxy-type=socks5',
    '--proxy-type=http',
    '--proxy-auth='':''',
    '--web-security=false',
]
    driver = webdriver.PhantomJS(
        desired_capabilities=dcap,
        # service_args=service_args
    )
    data = {}
    try :
        driver.get(url)
        driver.implicitly_wait(6)
        data['url'] = driver.find_element_by_xpath('//div[@class="search_result_single ng-scope"]/div[1]/div[1]/a').get_attribute("href")
        driver.get(data['url'])
        driver.implicitly_wait(6)
        #公司名
        data['name'] = driver.find_element_by_xpath('//div[@class="company_info_text"]/p').text.split(" ")[0]
        #官网网址
        try :
            data['domain'] = driver.find_element_by_xpath('//span/a[@ng-if="company.baseInfo.websiteList[0]"]').get_attribute("href")
        except :
            data['domain'] = driver.find_element_by_xpath('//span/span[@ng-hide="company.baseInfo.websiteList[0]"]').text
        #详细地址
        data['address'] = driver.find_element_by_xpath('//div[@class="company_info_text"]/span[4]').text.split(":")[1]
        #法人姓名
        try :
            data['corporation'] = driver.find_element_by_xpath('//p/a[@ng-if="company.baseInfo.legalPersonName"]').text
        except :
            data['corporation'] = driver.find_element_by_xpath('//p/span[@ng-hide="company.baseInfo.legalPersonName"]').text
        #电子邮件
        data['email'] = driver.find_element_by_xpath('//div[@class="company_info_text"]/span[2]').text.split(":")[1]
        #电话号码
        data['telephone'] = driver.find_element_by_xpath('//div[@class="company_info_text"]/span[1]').text.split(":")[1]
        #工商注册号
        data['business_id'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[2]/tbody/tr[1]/td[2]/div/span').text
        #组织机构代码
        data['organization_code'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[2]/tbody/tr[2]/td[2]/div/span').text
        #公司创建时间
        data['creation_date'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[1]/tbody/tr[4]/td[2]/p').text
        #公司经营范围
        data['business_scope'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[2]/tbody/tr[6]/td/div/span').text
        #所属行业
        data['industry_id'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[2]/tbody/tr[1]/td[1]/div/span').text
        #公司类型
        data['compay_type'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[2]/tbody/tr[2]/td[1]/div/span').text
        #公司状态
        data['state'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[1]/tbody/tr[4]/td[1]/p').text
        #企业核准日期
        data['approved_date'] = driver.find_element_by_xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[4]/table[2]/tbody/tr[4]/td[1]/div/span').text
        #营业期限
        try :
            data['operation_period'] = driver.find_element_by_xpath('//div/span[@ng-if="company.baseInfo.fromTime"]').text
        except :
            data['operation_period'] = driver.find_element_by_xpath('//div/span[@ng-if="!company.baseInfo.fromTime"]').text
        #注册资金（万）
        data['capital'] = driver.find_element_by_xpath('//td[@class="td-regCapital-value"]/p').text

    except Exception:
        pass

    driver.quit()
    if lock.acquire():
        for i in data:
            print(i+":"+data[i].strip())
        print "&"*30+"\n"
        lock.release()

def main():
    keywordlist = ['国际集装箱租赁有限公司','北京晶丽达影像技术有限公司','浙江盘石信息技术股份有限公司']
    lock = threading.Lock()

    mythreads = []
    for keyword in keywordlist:
        t = Mythread(tianyancha_spider,(keyword,lock))
        t.start()
        mythreads.append(t)

    # for mythread in mythreads:
    #     mythread.start()

    for i in mythreads:
        i.join()

if __name__ == '__main__':
    main()
