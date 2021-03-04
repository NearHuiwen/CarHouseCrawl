# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/8/5 14:44
from fake_useragent import UserAgent
import random

"""
    user_agent工具类
"""


class UA_Utils:
    def __init__(self):
        # 初始化fake_useragent
        self.fake_ua = UserAgent()

        # ua_list列表
        # 从fake_useragent获取谷歌UA池
        self.ua_list = self.fake_ua.data_browsers.get('chrome')

        # 获取UA列表数目
        self.ua_count = self.getUaCount()

        # 当前指针，用于轮询获取UA，每次调用不重复
        self.cur_pointer = 0


    # 轮询获取UA
    def getUaByPoll(self):
        self.cur_pointer += 1
        if (self.cur_pointer == self.ua_count):
            self.cur_pointer = 0
        return self.getUaByIndex(self.cur_pointer)

    # 获取UA列表数目
    def getUaCount(self):
        return len(self.ua_list)

    # 获取UA列表中获取一个
    def getUaByIndex(self, index):
        return self.ua_list[index]

    # 随机获取一个UA
    def randomGetUa(self):
        return self.getUaByIndex(random.randint(0, self.ua_count))

    # 使用fake_useragent 获取随机UA
    def getUaByFakeUseragent(self):
        return UserAgent().random


# if __name__ == '__main__':
#
#     ua_utils = UA_Utils()
#     for i in range (100):
#         print(ua_utils.getUaByPoll())

