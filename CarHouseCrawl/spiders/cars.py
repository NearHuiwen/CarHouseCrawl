import copy
import os
import re
import time

import scrapy
from lxml import etree
from CarHouseCrawl.items import CarhousecrawlItem
from CarHouseCrawl.utils.common import Common
from CarHouseCrawl.utils.log_utils import Log
from CarHouseCrawl.utils.mysql_manager import MySql_Utils
from CarHouseCrawl.utils.send_mail import SendMail
from scrapy.http.request import Request
from threading import Lock


class CarsSpider(scrapy.Spider):
    name = 'cars'

    def record_exception(self, exceptio_str):
        '''记录异常日志
        :param str:
        :return:
        '''
        self.mutex.acquire()
        self.record_exception_list.append(exceptio_str)
        self.mutex.release()

    # 添加总数
    def add_totalCount(self, count):
        self.mutex.acquire()
        self.totalCount += count
        self.mutex.release()

    def __init__(self):
        self.mySql_utils = MySql_Utils()
        self.pattern = re.compile(r'(?<=document.writeln\(\")(.*?)(?=\"\)\;)')
        # 爬取总数
        self.totalCount = 0
        self.mutex = Lock()  # 线程锁保证线程安全
        # 异常日志字符串
        self.record_exception_list = []

    def start_requests(self):
        all_brands = self.mySql_utils.get_all_brands()
        for index in range(len(all_brands)):
            brand = all_brands[index]
            req_url = f"https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId={brand['b_id']}%20&fctId=0%20&seriesId=0 "
            meta = {"brand": brand}
            print(f'准备爬取[{brand["b_name"]}]的信息\n')
            yield Request(url=req_url, method='GET', meta=meta,
                          callback=self.car_fct_parse,
                          dont_filter=True)

    def car_fct_parse(self, response):
        brand = response.meta.get('brand')
        html_str = self.pattern.findall(response.text.strip())[0]
        html_etree = etree.HTML(html_str, etree.HTMLParser())

        dl_list = html_etree.xpath(f"//li[@id='b{brand['b_id']}']/dl/*")
        fct = ''
        for dl_index in range(len(dl_list)):
            dl_item = dl_list[dl_index]
            if ("dt" == dl_item.tag):
                fct = dl_item.xpath("./a/text()")[0].strip()
            else:
                item = CarhousecrawlItem()
                s_id = dl_item.xpath("./a/@id")[0].strip()
                pattern = re.compile(r'(?<=series_)(\d+)')
                item['s_id'] = pattern.findall(s_id)[0]
                item['c_fct'] = fct
                item['b_id'] = brand['b_id']
                item['b_name'] = brand['b_name']
                series_url = dl_item.xpath("./a/@href")[0].strip()
                req_url2 = "https://car.autohome.com.cn" + series_url
                meta = {"carhousecrawlItem": item}
                print(f'准备爬取[{item["c_fct"]}]的第[{dl_index}]条信息\n')
                yield Request(url=req_url2, method='GET', meta=meta,
                              callback=self.car_series_parse,
                              dont_filter=True)

    def car_series_parse(self, response):
        item = response.meta.get('carhousecrawlItem')
        # html_etree2 = etree.HTML(response.text, etree.HTMLParser())
        cartab = response.xpath("//div[@class='cartab-title']")[0]
        # 汽车型号
        item["c_series_name"] = cartab.xpath("//div[@class='main-title']/a/text()").extract_first().strip()
        # # 发动机
        # item["c_engine"] = Common.spider_elements_text_by_xpath(cartab,
        #                                              "//ul[@class='lever-ul']/li[text()='发 动 机：']/span/a",
        #                                              " ")
        # 车身结构
        item["c_structure"] = Common.spider_elements_text_by_xpath(cartab,
                                                                   "//ul[@class='lever-ul']/li[text()='车身结构：']/a",
                                                                   " ")
        # 电动机
        item["c_electric_engine"] = Common.spider_xpath_is_null(cartab,
                                                                "//ul[@class='lever-ul']/li[text()='电 动 机：']/span/text()")
        # # 充电时间
        # item["c_charging_time"] = Common.spider_xpath_is_null(cartab,
        #                                                       "//ul[@class='lever-ul']/li[text()='充电时间：']/span/text()")
        # 续航里程
        item["c_endurance_mileage"] = Common.spider_xpath_is_null(cartab,
                                                                  "//ul[@class='lever-ul']/li[text()='续航里程：']/span/text()")
        _time = int(round(time.time() * 1000))
        req_url = f"https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value={item['s_id']}&_={_time}"
        meta = {"carhousecrawlItem": item}
        print(f'准备爬取[{item["c_fct"]}][{item["c_series_name"]}]的车型信息\n')
        yield Request(url=req_url, method='GET', meta=meta,
                      callback=self.car_spec_parse,
                      dont_filter=True)

    def car_spec_parse(self, response):
        item0 = response.meta.get('carhousecrawlItem')
        res_json = response.json()
        yearitems = res_json.get("result").get("yearitems")
        for y_index in range(len(yearitems)):
            yearitem = yearitems[y_index]
            specitems = yearitem.get("specitems")
            for sp_index in range(len(specitems)):
                specitem = specitems[sp_index]
                c_id = specitem.get("id")
                if (not self.mySql_utils.is_exist(c_id)):
                    item = copy.deepcopy(item0)
                    item["c_id"] = c_id
                    item["c_spec_name"] = specitem.get("name")
                    req_url = f"https://www.autohome.com.cn/spec/{item['c_id']}/"
                    meta = {"carhousecrawlItem": item}
                    print(f'准备爬取[{item["c_id"]}][{item["c_spec_name"]}]的详情信息\n')
                    yield Request(url=req_url, method='GET', meta=meta,
                                  callback=self.car_detail_parse,
                                  dont_filter=True)

    def car_detail_parse(self, response):
        item = response.meta.get('carhousecrawlItem')
        # 级别
        item["c_level"] = response.xpath(
            "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='级别']]/p/text()").extract_first().strip()
        # 汽车图片
        item["c_img_url"] = "https:" + response.xpath("//span[@class='scaleimg']//img/@src").extract_first().strip()
        # 变速箱
        item["c_gearbox"] = Common.spider_elements_text_by_xpath(response,
                                                                 "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='变速箱']]/p",
                                                                 " ")
        # 综合油耗(工信部)
        item["c_fuel_consump"] = Common.spider_elements_text_by_xpath(response,
                                                                      "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='综合油耗(工信部)']]/p",
                                                                      " ")
        # 最大扭矩
        item["c_max_torque"] = Common.spider_elements_text_by_xpath(response,
                                                                    "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='最大扭矩']]/p",
                                                                    " ")
        # 环保标准
        item["c_envi_stan"] = Common.spider_elements_text_by_xpath(response,
                                                                   "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='环保标准']]/p",
                                                                   " ")
        # 最大功率
        item["c_max_power"] = Common.spider_elements_text_by_xpath(response,
                                                                   "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='最大功率']]/p",
                                                                   " ")
        # 发动机/排量
        item["c_engine"] = Common.spider_elements_text_by_xpath(response,
                                                                "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='排量']]/p",
                                                                " ")
        # 续航里程
        c_endurance_mileage = Common.spider_elements_text_by_xpath(response,
                                                                   "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='续航里程']]/p",
                                                                   " ")
        if (c_endurance_mileage):
            item["c_endurance_mileage"] = c_endurance_mileage
        # 能源类型
        item["c_energy_type"] = Common.spider_elements_text_by_xpath(response,
                                                                     "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='能源类型']]/p",
                                                                     " ")
        # 慢充时间
        item["c_slow_charging_time"] = Common.spider_elements_text_by_xpath(response,
                                                                            "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='慢充时间']]/p",
                                                                            " ")
        # 快充时间
        item["c_fast_charging_time"] = Common.spider_elements_text_by_xpath(response,
                                                                            "//div[@class='spec-content']/div[@class='param-list']/div[span[text()='快充时间']]/p",
                                                                            " ")
        yield item

    def close(spider, reason):
        '''调用异常日志发送
        :param reason:
        :return:
        '''
        spider.mySql_utils.connect_close()
        if (spider.record_exception_list):
            smtp_subject = "汽车之家爬虫异常日志"
            path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs'),
                                f"{smtp_subject}{time.strftime('%Y-%m-%d_%H-%M-%S')}.log")
            log = Log(path)
            # 取前十个
            for record_exception in spider.record_exception_list[:10]:
                log.error(record_exception)
            SendMail(
                smtp_subject=smtp_subject,
                smtp_body='日志地址：' + path, smtp_file=path).send_mail()
