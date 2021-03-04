# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarhousecrawlItem(scrapy.Item):
    # define the fields for your item here like:
    c_id = scrapy.Field()  # 汽车ID
    b_id = scrapy.Field()  # 品牌ID
    s_id = scrapy.Field()  # 车系ID
    b_name = scrapy.Field()  # 品牌名
    c_fct = scrapy.Field()  # 品牌分支
    c_series_name = scrapy.Field()  # 车系
    c_spec_name = scrapy.Field()  # 车型
    c_img_url = scrapy.Field()  # 汽车图片
    c_level = scrapy.Field()  # 级别
    c_engine = scrapy.Field()  # 发动机/排量
    c_gearbox = scrapy.Field()  # 变速箱
    c_structure = scrapy.Field()  # 车身结构
    c_electric_engine = scrapy.Field()  # 电动机
    # c_charging_time = scrapy.Field()  # 充电时间
    c_endurance_mileage = scrapy.Field()  # 续航里程
    c_fuel_consump = scrapy.Field()  # 综合油耗(工信部)
    c_max_torque = scrapy.Field()  # 最大扭矩
    c_envi_stan = scrapy.Field()  # 环保标准
    c_max_power = scrapy.Field()  # 最大功率
    # c_emission = scrapy.Field()  # 排量
    c_energy_type = scrapy.Field()  # 能源类型
    c_slow_charging_time = scrapy.Field()  # 慢充时间
    c_fast_charging_time = scrapy.Field()  # 快充时间
