# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/12/15 14:33
import os

import pymysql
import logging
import configparser

from dbutils.pooled_db import PooledDB

"""
 数据库连接池相关
"""



class MySQLConnection(object):
    """
    数据库连接池代理对象
    查询参数主要有两种类型
    第一种：传入元祖类型,例如(12,13),这种方式主要是替代SQL语句中的%s展位符号
    第二种: 传入字典类型,例如{"id":13},此时我们的SQL语句需要使用键来代替展位符,例如：%(name)s
    """
    def __init__(self,dbName="local1"):
        # 读取数据库配置信息
        config = configparser.RawConfigParser()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.conf')
        config.read(path, encoding='UTF-8')
        sections = config.sections()
        # 数据库工厂
        dbFactory = {}
        for dbName in sections:
            # 读取相关属性
            maxconnections = config.get(dbName, "maxconnections")
            mincached = config.get(dbName, "mincached")
            maxcached = config.get(dbName, "maxcached")
            host = config.get(dbName, "host")
            port = config.get(dbName, "port")
            user = config.get(dbName, "user")
            password = config.get(dbName, "password")
            database = config.get(dbName, "database")
            databasePooled = PooledDB(creator=pymysql,
                                      maxconnections=int(maxconnections),
                                      mincached=int(mincached),
                                      maxcached=int(maxcached),
                                      blocking=True,
                                      cursorclass=pymysql.cursors.DictCursor,
                                      host=host,
                                      port=int(port),
                                      user=user,
                                      password=password,
                                      database=database)
            dbFactory[dbName] = databasePooled

        self.connect = dbFactory[dbName].connection()
        self.cursor = self.connect.cursor()
        logging.debug("获取数据库连接对象成功,连接池对象:{}".format(str(self.connect)))

    def execute(self,sql,param=None):
        """
        基础更新、插入、删除操作
        :param sql:
        :param param:
        :return: 受影响的行数
        """
        ret=None
        try:
            if param==None:
                ret=self.cursor.execute(sql)
            else:
                ret=self.cursor.execute(sql,param)
        except TypeError as te:
            logging.debug("类型错误")
            logging.exception(te)
        return ret
    def query(self,sql,param=None):
        """
        查询数据库
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回集合
        """
        self.cursor.execute(sql,param)
        result=self.cursor.fetchall()
        return result
    def queryOne(self,sql,param=None):
        """
        查询数据返回第一条
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回第一条数据的字典
        """
        result=self.query(sql,param)
        if result:
            return result[0]
        else:
            return None
    def listByPage(self,sql,current_page,page_size,param=None):
        """
        分页查询当前表格数据
        :param sql: 查询SQL语句
        :param current_page: 当前页码
        :param page_size: 页码大小
        :param param:参数
        :return:
        """
        countSQL="select count(*) ct from ("+sql+") tmp "
        logging.debug("统计SQL:{}".format(sql))
        countNum=self.count(countSQL,param)
        offset=(current_page-1)*page_size
        totalPage=int(countNum/page_size)
        if countNum % page_size>0:
            totalPage = totalPage + 1
        pagination={"current_page":current_page,"page_size":page_size,"count":countNum,"total_page":totalPage}
        querySql="select * from ("+sql+") tmp limit %s,%s"
        logging.debug("查询SQL:{}".format(querySql))
        # 判断是否有参数
        if param==None:
            # 无参数
            pagination["data"]=self.query(querySql,(offset,page_size))
        else:
            # 有参数的情况,此时需要判断参数是元祖还是字典
            if isinstance(param,dict):
                # 字典的情况,因此需要添加字典
                querySql="select * from ("+sql+") tmp limit %(tmp_offset)s,%(tmp_pageSize)s"
                param["tmp_offset"]=offset
                param["tmp_pageSize"]=page_size
                pagination["data"]=self.query(querySql,param)
            elif isinstance(param,tuple):
                # 元祖的方式
                listtp=list(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"]=self.query(querySql,tuple(listtp))
            else:
                # 基础类型
                listtp=[]
                listtp.append(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"]=self.query(querySql,tuple(listtp))
        return pagination
    def count(self,sql,param=None):
        """
        统计当前表记录行数
        :param sql: 统计SQL语句
        :param param: 参数
        :return: 当前记录行
        """
        ret=self.queryOne(sql,param)
        count=None
        if ret:
            for k,v in ret.items():
                count=v
        return count

    def insert(self,sql,param=None):
        """
        数据库插入
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql,param)
    def update(self,sql,param=None):
        """
        更新操作
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql,param)
    def delete(self,sql,param=None):
        """
        删除操作
        :param sql: 删除SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql,param)
    def batch(self,sql,param=None):
        """
        批量插入
        :param sql: 插入SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.cursor.executemany(sql,param)
    def commit(self,param=None):
        """
        提交数据库
        :param param:
        :return:
        """
        if param==None:
            self.connect.commit()
        else:
            self.connect.rollback()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
        logging.debug("释放数据库连接")
        return None