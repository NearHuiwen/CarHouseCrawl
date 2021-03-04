# -*- coding: utf-8 -*-
from CarHouseCrawl.utils.mysql_connection import MySQLConnection

"""
MySQL数据库控制工具
"""


class MySql_Utils(object):
    def __init__(self):
        self.connect = MySQLConnection("local1")

    def connect_close(self):
        self.connect.close()
        print("MySQL工具类断开连接")

    def __del__(self):
        self.connect.close()
        print("MySQL工具类对象被回收")

    # 添加/替换品牌信息
    def replace_brand_one(self, item):
        sql = "REPLACE INTO carhouse_brand_info(b_id,b_name,b_url,b_img) VALUES (%(b_id)s,%(b_name)s,%(b_url)s,%(b_img)s)"
        effect_num = self.connect.insert(sql, item)
        self.connect.commit()
        return effect_num

    # 添加/替换汽车信息
    def replace_car_one(self, item):
        params = []
        sql_h = "REPLACE INTO carhouse_car_info("
        sql_e = ") VALUES ("
        for k, v in item.items():
            params.append(v)
            sql_h += k + ','
            sql_e += '%s,'
        sql = sql_h[:-1] + sql_e[:-1] + ")"
        effect_num = self.connect.insert(sql, params)
        self.connect.commit()
        return effect_num

    # 根据url,判断是否存在
    def is_exist(self, c_id):
        params = [c_id]
        sql = "SELECT COUNT(1) FROM carhouse_car_info WHERE c_id=%s"
        effect_count = self.connect.queryOne(sql, params)
        if (0 < effect_count.get('COUNT(1)', 0)):
            return True
        else:
            return False

    def get_all_brands(self):
        sql = "SELECT * FROM carhouse_brand_info"
        return self.connect.query(sql)


# if __name__ == '__main__':
#     mySql_Utils = MySql_Utils()
    # aaa=mySql_Utils.get_all_brands()
    # aaa = mySql_Utils.is_exist(20056)
    # mySql_Utils.connect_close()
    # pass
