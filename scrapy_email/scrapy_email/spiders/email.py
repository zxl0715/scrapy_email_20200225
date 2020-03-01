# -*- coding: utf-8 -*-
import scrapy

# PS E:\MyData\zxl0715\Python\scrapy_email_20200225\scrapy_email\scrapy_email\spiders> scrapy  crawl email


class EmailSpider(scrapy.Spider):
    name = 'email'
    allowed_domains = ['mail.263.net']  # ['email.org']
    start_urls = ['https://mail.263.net']  # ['http://email.org/']

    def parse(self, response):
        """
        @url https://mail.263.net
        """
        print(response.url)

        print(response.body.decode('utf-8'))

        semial = response.xpath(
            '/html/body/div[2]/div[2]/div/div[3]/div/div[4][1]/text()').extract()
        print('爬虫获取到的内容：{0}'.format(semial))
        self.log('邮箱地址:%s' % semial)

  
        # pass

    def start_requests(self):
        urls = ['https://mail.263.net']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        return super().start_requests()

    def __init__(self, companyname=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.companyname = companyname
        driver = None  # 实例selenium
        cookies = None  # 用来保存cookie
