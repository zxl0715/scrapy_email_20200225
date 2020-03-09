# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyEmailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index_Num = scrapy.Field()
    # 收件邮件名称
    emial_name = scrapy.Field()
    # 收件邮件地址
    emial_address = scrapy.Field()
    # 发件邮件地址
    emial_from_name = scrapy.Field()
    # 发件邮件地址
    emial_from = scrapy.Field()
    # 发件时间
    emial_sender_time = scrapy.Field()
    # 邮件标题
    emial_sender_title = scrapy.Field()
    # 程序执行时间
    exec_time = scrapy.Field()
    # 程序请求url
    response_url = scrapy.Field()
    # pass
