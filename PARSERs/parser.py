# -*-coding=utf-8-*-
__author__ = 'LiuJingYuan'
from lxml import etree
class lxmlparser():
    def __init__(self):
        self.data = {}

    def JSparser(self,html,gsurl):
        try:
            tree = etree.HTML(html)
            # 公司url
            self.data['url'] = gsurl
            # 公司名
            self.data['name'] = tree.xpath("//div[@class='company_info_text']/div")[0].text.strip()
            # 官网网址
            try:
                self.data['domain'] = tree.xpath('//span/a[@ng-if="company.websiteList"]/@href')[0].strip()
            except:
                self.data['domain'] = ''.join(tree.xpath('//span/span[@ng-bind-html="company.websiteList?company.websiteList:\u6682\u65e0"]'))
            # 详细地址
            self.data['address'] = tree.xpath('//div[@class="company_info_text"]/span[4]/text()[2]')[0].strip()
            # 法人姓名
            try:
                self.data['corporation'] = tree.xpath('//div/a[@ng-if="company.legalPersonName"]/text()')[0].strip()
            except:
                self.data['corporation'] = tree.xpath('//div/span[@ng-hide="company.legalPersonName"]/text()')[0].strip()
            # 电话号码
            self.data['email'] =  tree.xpath('//div[@class="company_info_text"]/span[2]/text()[2]')[0].strip()
            # 邮箱
            self.data['telephone'] = tree.xpath('//div[@class="company_info_text"]/span[1]/text()[2]')[0].strip()
            # 工商注册号
            self.data['business_id'] = tree.xpath('//tbody/tr[1]/td[1]/div/span')[0].text.strip()
            # 组织机构代码
            self.data['organization_code'] = tree.xpath('//tbody/tr[1]/td[2]/div/span')[0].text.strip()
            # 公司创建时间
            self.data['creation_date'] = tree.xpath('//html/body/div[1]/div[2]/div/div/div/div[1]/div/div[5]/div[3]/div/div[2]/div[2]')[0].text.strip()
            # 公司经营范围
            self.data['business_scope'] = tree.xpath('//tbody/tr[6]/td/div/span/span/text()')[0].strip()
            # 所属行业
            self.data['industry_id'] = tree.xpath('//tbody/tr[3]/td[1]/div/span')[0].text.strip()
            # 公司类型
            self.data['compay_type'] = tree.xpath('//tbody/tr[2]/td[2]/div/span')[0].text.strip()
            # 公司状态
            self.data['state'] =  tree.xpath('//html/body/div[1]/div[2]/div/div/div/div[1]/div/div[5]/div[4]/div/div[2]/div[2]')[0].text.strip()
            # 企业核准日期
            self.data['approved_date'] =  tree.xpath('//tbody/tr[4]/td[1]/div/span')[0].text.strip()
            # 营业期限
            try:
                self.data['operation_period'] =  tree.xpath('//div/span[@ng-if="company.fromTime"]')[0].text.strip()
            except:
                self.data['operation_period'] =  tree.xpath('//div/span[@ng-if="!company.fromTime"]')[0].text.strip()
            # 注册资金（万）
            self.data['capital'] = tree.xpath('//html/body/div[1]/div[2]/div/div/div/div[1]/div/div[5]/div[2]/div/div[2]/div[2]')[0].text.strip()
        except Exception as e:
            print e
        # print self.data
        return self.data
if __name__ == '__main__':
    pass
