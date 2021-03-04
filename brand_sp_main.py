# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/12/3 10:39
import re

import requests
from lxml import etree

from CarHouseCrawl.utils.mysql_manager import MySql_Utils


class Car:
    def __init__(self):
        self.mySql_utils = MySql_Utils()
        self.pattern = re.compile(r'(?<=document.writeln\(\")(.*?)(?=\"\)\;)')
    def get_brands(self):
        req_url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0"
        res=requests.get(req_url)
        res.encoding = 'gbk'
        html_str = self.pattern.findall(res.text.strip())[0]
        html_etree = etree.HTML(html_str, etree.HTMLParser())
        li_list=html_etree.xpath("//li")

        for index in range(len(li_list)):
            li_item=li_list[index]
            item={}
            b_id=li_item.xpath("./@id")[0].strip()
            pattern = re.compile(r'(?<=b)(\d+)')
            b_id=pattern.findall(b_id)[0]
            item["b_id"]=b_id
            item["b_url"] = li_item.xpath(".//a/@href")[0].strip()
            item["b_name"] = li_item.xpath(".//a/text()")[0].strip()
            req_url2 = "https://car.autohome.com.cn" + item["b_url"]
            res2 = requests.get(req_url2)
            html_etree2 = etree.HTML(res2.text, etree.HTMLParser())
            item["b_img"] = "https:"+html_etree2.xpath("//div[@class='carbradn-pic']/img/@src")[0].strip()
            self.mySql_utils.replace_brand_one(item)
            print(str(item))
        self.mySql_utils.connect_close()
        return  html_etree


if __name__ == '__main__':

    car=Car()

    html_etree=car.get_brands()


    pass
