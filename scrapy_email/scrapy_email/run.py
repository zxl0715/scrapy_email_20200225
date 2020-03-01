from scrapy.cmdline import execute
import sys
import os

# ============================================
# 启动爬虫入口
# ============================================

# 获取当前脚本路径
dirpath = os.path.dirname(os.path.abspath(__file__))
dirpath += '\spiders'
print(dirpath)
# 添加环境变量
sys.path.append(dirpath)
# e:\MyData\zxl0715\Python\scrapy_email_20200225\scrapy_email\scrapy_email\spiders
# E:\MyData\zxl0715\Python\scrapy_email_20200225\scrapy_email\scrapy_email\spiders> scrapy crawl email
# 启动爬虫，第三个参数为爬虫名称
# execute(['scrapy','crawl','login'])
execute(['scrapy', 'crawl', 'EmialFiled'])
# execute(['scrapy','crawl','email'])
