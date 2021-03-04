# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/8/12 14:15


from scrapy.cmdline import execute
import sys
import os



if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["srcapy", "crawl", "cars"])
