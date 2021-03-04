# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from CarHouseCrawl.items import CarhousecrawlItem


class CarhousecrawlPipeline:
    def process_item(self, item, spider):
        if (isinstance(item, CarhousecrawlItem)):
            effect_num=spider.mySql_utils.replace_car_one(item)
            if(0<effect_num):
                spider.add_totalCount(1)
                print(f'爬取[{item["c_spec_name"]}]的信息成功，目前已爬取共[{spider.totalCount}]条数据\n')
            else:
                print(f'爬取[{item["c_spec_name"]}]的信息失败，目前已爬取共[{spider.totalCount}]条数据\n')

        return item
