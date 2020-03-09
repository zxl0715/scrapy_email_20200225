# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2  # PostgreSQL


class ScrapyEmailPGPipeline(object):
    def __init__(self):
        # def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'gszh8899'
        database = 'wisdomMarket'

        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        # 写入多行（数据）
        self.cur.excute("INSERT INTO public.scrapy_email_263(id, to_email_name, to_email_address, from_email_name, form_email_address, sender_time, title, exec_time, response_url) VALUES(0, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ", (item['emial_name'], item['emial_address'], item['emial_from_name'], item['emial_from'], item['emial_sender_time'],
                                                                                                                                                                                                                                                  item['emial_sender_title'], item['exec_time'], item['response_url']))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        print("保存文件成功，处理结束")
        self.cur.colse()
        self.connection.colse()
