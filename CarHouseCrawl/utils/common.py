# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/8/5 13:55



class Common:
     # lxml xpath爬取,判断是否为空
    @staticmethod
    def spider_xpath_is_null(response, path):
        list = response.xpath(path)
        if (list):
            return list.extract_first().strip()
        else:
            return ""


    # xpath爬取（包含换行符）
    @staticmethod
    def spider_elements_text_by_xpath(response, path, separate=""):
        list = response.xpath(path)
        if (len(list) > 0):
            for index in range(len(list)):
                list[index] = list[index].xpath('./text()').extract_first().strip()
            data = separate.join(list)
            return data
        else:
            return ""

    # lxml xpath爬取（包含换行符）
    @staticmethod
    def lxml_data_by_xpath(response, path,separate=""):
        list = response.xpath(path)
        if (len(list) > 0):
            for index in range(len(list)):
                list[index] = list[index].strip()
            data = separate.join(list)
            return data
        else:
            return ""

     # lxml xpath爬取,判断是否为空
    @staticmethod
    def lxml_xpath_is_null(response, path):
        list = response.xpath(path)
        if (list):
            return list[0].strip()
        else:
            return ""


