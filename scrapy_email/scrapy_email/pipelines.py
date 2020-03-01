# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class ScrapyEmailPipeline(object):
    def __init__(self):
        # 初始化一个文件
        file_name = 'email_20200301.csv'
        self.file_cvs = open(file_name, "a+", encoding='utf-8', newline='')
        b_csv = csv.writer(self.file_cvs)  # 创建 csv 对象
        headers = [('收件邮件名称', '收件邮件地址', '发件邮件地址', '发件邮件地址',
                    '发件时间', '邮件标题', '程序执行时间', '程序请求url')]
        b_csv.writerows(headers)  # 写入一行（标题）

    def process_item(self, item, spider):
        # f = file('/root/zhuanti.csv','a+')
        # writer = csv.writer(f)
        # writer.writerow((item['collection_name'],item['collection_description'],item['collection_article_count'],item['collection_attention_count']))
        # self.data_write_csv('email_20200301.csv', item)
        datas=item
        b_csv = csv.writer(self.file_cvs)  # 创建 csv 对象
        b_csv.writerow((datas['emial_name'], datas['emial_address'], datas['emial_from_name'], datas['emial_from'], datas['emial_sender_time'],
                        datas['emial_sender_title'], datas['exec_time'], datas['response_url']))  # 写入多行（数据）

        return item

    def close_spider(self,spider):
        print("保存文件成功，处理结束")
        self.file_cvs.close()

    def data_write_csv(self, file_name, datas):  # file_name为写入CSV文件的路径，datas为要写入数据列表

        with open(file_name, "a+", encoding='utf-8', newline='') as b:
            b_csv = csv.writer(b)  # 创建 csv 对象
            # b_csv.writerow(headers) #写入一行（标题）
            b_csv.writerow((datas['emial_name'], datas['emial_address'], datas['emial_from'], datas['emial_sender_time'],
                            datas['emial_sender_title'], datas['exec_time'], datas['response_url']))  # 写入多行（数据）

            # b_csv.writerow(dict(datas))
