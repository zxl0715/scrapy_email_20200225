# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import os
from urllib import parse
from scrapy.cmdline import execute
import sys
import time
import csv
# from items import ScrapyEmailItem
from items import ScrapyEmailItem


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['mail.263.net']
    start_urls = ['https://mail.263.net']
    user_email = "******@163.com"
    user_email_passwd = "$761;$491;$691;$501;$711;$511;$651;$521;$461;$461;"
    sid = ''
    page_num = 314  # 314
    emial_num = 6263  # 6263
    indexNum = 0

    return_emial = 0
    data = []

    def start_requests(self):
        # 1.首先进入登录页面
        url = "http://mail.263.net/"
        returnlst = [Request(url, callback=self.start_login)]
        print("完成 @！！！！！！！！！！！！！！！！！！！！！")
        return returnlst

    def start_login(self, response):
        # 2.开始登录
        """
        $761;$491;$691;$501;$711;$511;$651;$521;$461;$461;
        """
        import time
        import datetime

        t = time.time()
        mst = str(int(round(t * 1000)))
        loginurl = "https://mail.263.net/xmweb?host=mail.263.net&_t={0}".format(
            mst)

        # header信息
        unicornHeader = {
            'Host': 'mail.263.net',
            'Referer': 'http://mail.263.net/',
        }

        return [
            FormRequest(
                loginurl,
                headers=unicornHeader,
                formdata={"chr": "gb",
                          "func": "login",
                          "isp_domain": "",
                          "verifycookie": "",
                          "verifyip": "",
                          "buttonType": "1",
                          "usr": "gloria",
                          "domain": "legapower.com",
                          "domainType": "wm",
                          "encode": "on",
                          "username": self.user_email,
                          "pass": self.user_email_passwd,
                          "safelogin": "on",
                          }, callback=self.parse_get_email_home)]

    def after_login(self, response):
        # 3.登陆后验证是否登录成功！
        print("登陆后验证是否登录成功！")
        print(response.url)

        print(response.body.decode('utf-8'))

        semial = response.xpath('//*[@id="email"]/text()').extract()
        return parse_get_email_home(self, response)
        # return [Request(response.url, callback=self.parse_get_email_home, errback=self.parse_error,)]

        # if str(semial).find(user_email) > 0:
        #     # 在登录页找到用户的邮箱地址，说明登录成功
        #     return [Request(self.start_urls[0], callback=self.parse_get_email_home, errback=self.parse_error,)]
        # else:
        #     self.logger.error('登录失败！')
        # return

    def parse_get_email_home(self, response):
        # 进入邮箱主页，查询邮件 发件人包含为 sales08 的邮件列表信息
        semial = str(parse.parse_qs(
            parse.urlparse(response.url).query)['usr'][0])
        # if str(semial).find(user_email) > 0:
        #     # 在登录页找到用户的邮箱地址，说明登录成功
        #     return [Request(self.start_urls[0], callback=self.parse_get_email_home, errback=self.parse_error,)]
        # else:
        #     self.logger.error('登录失败！')
        # return
        print("登陆后验证是否登录成功！")
        # 获取url参数
        params = parse.parse_qs(parse.urlparse(response.url).query)
        sid = params['sid'][0]
        self.sid = sid
        # print('返回的sid：%s' % sid)
        # print(os.path.split(response.url)[-1])

        # print('返回的地址：')
        # print(response.url)
        # print('返回的内容：')
        # print(response.body.decode('utf-8'))

        url = "https://mail.263.net/wm2e/mail/mailIndex/mailIndexAction_indexList.do"
        returnlist = [FormRequest(url, formdata={
            "folderId": "",
            "type": "",
            "qstr": "{ \"ifQuick\" : \"0\" , \"sender\" : \"sales08\" }",
            "usr": self.user_email,
            "sid": self.sid,
            "start": "",
            "keyInfo": "",
            "sort": "",
        }, callback=self.parse_get_email_list)]
        print("完成 222222@！！！！！！！！！！！！！！！！！！！！！")
        return returnlist

    def parse_get_email_list(self, response):
        # 获取查询到的邮件列表信息

        # print('返回的地址：')
        # print(response.url)
        # print('返回的内容：')
        # print(response.body.decode('utf-8'))

        page_num = response.xpath(
            '/html/body/table/tr/td/div[2]/div/a/span[1]/text()').extract_first()  # 获取总页码
        page_num = str(page_num.split('/')[1]).replace('\']', '')

        self.page_num = int(page_num)
        # self.page_num = 2  # 0715
        print('返回查询到邮箱的页数：%s' % page_num)
        _emial_num = response.xpath(
            '/html/head/script[5]').extract_first()
        emial_num = _emial_num[_emial_num.find('total = '):_emial_num.find(
            ';', _emial_num.find('total = '))].replace('total = ', '')
        self.emial_num = int(emial_num)
        print('查找到邮件封数:%s' % self.emial_num)
        base_url = "https://mail.263.net/wm2e/mail/mailIndex/mailIndexAction_indexList.do"
        url = (
            base_url+"?usr={0}&sid={1}&12").format(self.user_email, self.sid)
        for item in range(self.page_num):
            pageNo = item+1
            email_list = FormRequest(url, formdata={
                "pageNo": str(pageNo),
                "qstr": '{ "ifQuick" : "0" , "sender" : "sales08" }',
                "sortStr": '{"time":"desc"}',
                "fstr": "{}",
                "folderId": "",
                "type": "",
                "fullSearchIfmIsHide": "null",
            }, callback=self.parse_get_email_read)
            yield email_list

        return data_write_csv('email_'+self.user_email+'.csv', self.data)

    def parse_get_email_read(self, response):
        # 读取邮件（每页20条）
        # //*[@id = "contList2"]/ul[1]/li[1]/span[2]/input
        # //*[@id = "contList2"]/ul[2]/li[1]/span[2]/input

        print('返回的地址：')
        print(response.url)
        # print('返回的内容：')
        # print(response.body.decode('utf-8'))
        # 获取页面索引
        # params = parse.parse_qs(parse.urlparse(response.url).query)
        # pageNo = int(params['indexNum'])
        pageNo = str(response.request.body,
                     'utf-8').split('&')[0].split('=')[1]  # 获取页面索引
        pageNo = int(pageNo)
        base_url = "https://mail.263.net/wm2e/mail/mailOperate/mailOperateAction_mailInfo.do"
        indexNum = 1  # 选中的邮件缓存中索引

        for item in range(20):
            index = item+1
            emailIdentity = response.xpath(
                '//*[@id="contList2"]/ul[{0}]/li[1]/span[2]/input/@value'.format(index)).extract_first()
            # emailIdentity=response.xpath(
            # '//*[@id = "contList2"]/ul[{0}]/li[1]/span[2]/input/text()'.format(index)).extract()

            indexNum = (pageNo-1)*20+index
            if indexNum > self.emial_num:
                break
            params_url = "mailOperateType=read"
            params_url = params_url+"&emailIdentity="+emailIdentity
            params_url = params_url+"&selfFolderId=10"
            params_url = params_url+"&usr="+self.user_email
            params_url = params_url+"&sid="+self.sid
            params_url = params_url+"&statFlag=2"
            params_url = params_url+"&starred=0"
            params_url = params_url+"&waited=0"
            params_url = params_url+"&floderType=10"
            params_url = params_url+"&indexNum="+str(indexNum)
            params_url = params_url+"&reachStoragePoint=true"
            params_url = params_url+"&undoSend="
            params_url = params_url+"&encryptMail=false"
            params_url = params_url+"&mailPasswdStatus=0"
            params_url = params_url+"&securityMark=0"
            params_url = params_url+"&securityType=0"
            params_url = params_url+"&frameJump=1"

            url = base_url+'?'+params_url
            email_list = FormRequest(url, formdata={
                "pageNo": str(pageNo),
                "qstr": "{ \"ifQuick\" : \"0\" , \"sender\" : \"sales08\" }",
                "sortStr": "{\"time\":\"desc\"}",
                "fstr": "{}",
                "folderId": "",
                "type": "",
                "fullSearchIfmIsHide": "null",
            }, callback=self.parse_get_email_info)
            yield email_list
        return

    def parse_get_email_info(self, response):
        # 获取邮件
        emial_data = []
        self.return_emial = self.return_emial+1
        exec_time = str(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
        print('邮件编号{0}, 时间：{1}'.format(self.return_emial, exec_time))
        print('1邮件的url：%s' % response.url)
        # print('2返回的内容：')
        # print(response.body.decode('utf-8'))
        emial_from = response.xpath(
            '//*[@id="mailAddG"]/text()').extract_first()
        emial_address = response.xpath(
            '//*[@id="readMailBox"]/div[2]/div[2]/ul/li[3]/span/span[2]/text()').extract_first()
        emial_name = response.xpath(
            '//*[@id="readMailBox"]/div[2]/div[2]/ul/li[3]/span/span[1]/text()').extract_first()

        print('2邮件地址%s' % emial_address)
        emial_sender_time = response.xpath(
            '//*[@id="readMailBox"]/div[2]/div[2]/ul/li[1]/div[5]/span[3]/text()').extract_first()
        emial_sender_title = response.xpath(
            '//*[@id="mailTit"]/div[1]/span[2]/text()').extract_first()
        emial_data.append(emial_name)
        emial_data.append(emial_address)
        emial_data.append(emial_from)
        emial_data.append(emial_sender_time)
        emial_data.append(emial_sender_title)
        emial_data.append(exec_time)
        emial_data.append(response.url)
        self.data.append(emial_data)

        scrapy_emial_item = ScrapyEmailItem(
            emial_name=emial_name, emial_address=emial_address, emial_from=emial_from, emial_sender_time=emial_sender_time,
            emial_sender_title=emial_sender_title, exec_time=exec_time, response_url=response.url)
        yield scrapy_emial_item

    def parse_error(self, response):
        print('请求获取的内容错误！！！！！！！！！！！！！')
        # pass
        return


def data_write_csv(file_name, datas):  # file_name为写入CSV文件的路径，datas为要写入数据列表

    with open(file_name, "w", encoding='utf-8', newline='') as b:
        b_csv = csv.writer(b)  # 创建 csv 对象
        # b_csv.writerow(headers) #写入一行（标题）
        b_csv.writerows(datas)  # 写入多行（数据）
    print("保存文件成功，处理结束")


if __name__ == '__main__':
    # 获取当前脚本路径
    dirpath = os.path.dirname(os.path.abspath(__file__))
    dirpath += '\spiders'
    print(dirpath)
    # 添加环境变量
    sys.path.append(dirpath)
    # e:\MyData\zxl0715\Python\scrapy_email_20200225\scrapy_email\scrapy_email\spiders
    # E:\MyData\zxl0715\Python\scrapy_email_20200225\scrapy_email\scrapy_email\spiders> scrapy crawl email
    # 启动爬虫，第三个参数为爬虫名称
    execute(['scrapy', 'crawl', 'login'])
