汽车之家爬虫(汽车品牌详情、车型详情、品牌和车型的图片下载地址)
===============

> 项目普及技术：Scrapy、MySql

请在Python3下运行(版本太低可能会出现不兼容，本人用的是3.7版本)

运行前请配置好MySql相关数据
数据库脚本在"数据库"文件夹里，数据库名：carhouse

## 注意

（截止版本2021年3月，即后面可能接口出现更新，可能会过时，请谅解）

源码仅作为和大家一起**学习Python**使用，你可以免费: 拷贝、分发和派生当前源码。

但你用于*商业目的*及其他*恶意用途*，作者也不会管你，耗子尾汁



## 开发环境安装

首先，配置好你的Python、MySql环境

本人用的是pipenv虚拟环境
如果你已有虚拟环境以下可忽略
安装
```bash
$ pip install -i https://pypi.douban.com/simple pipenv
```
创建文件夹“CarHouseCrawl”（项目放在这里）
创建虚拟环境
```bash
$ cd CarHouseCrawl
$ pipenv install
```

进入虚拟环境
```bash
$ cd CarHouseCrawl
$ pipenv shell
```

导入项目，也可直接下载覆盖CarHouseCrawl文件夹
```bash
$ git clone https://github.com/NearHuiwen/CarHouseCrawl.git
```

安装项目所需要的包

大功告成,直接跳到下一节配置和运行.

## 配置和运行

首先部署MySql数据库

数据库脚本在文件里，数据库名：carhouse

注意：该脚本包含已爬完的数据，如需要可清空

在db.conf 配置MySql账号和密码

在send_mail.py 配置异常邮箱警告（可不配置）

## 运行步骤：
1、先运行brand_sp_main.py 爬取全部汽车品牌，如下图：

<img src="https://raw.githubusercontent.com/NearHuiwen/CarHouseCrawl/master/CarHouseCrawl/picture/a1.png" width="800">

2、再运行main.py 根据汽车品牌，爬取所有车型，如下图：

<img src="https://raw.githubusercontent.com/NearHuiwen/CarHouseCrawl/master/CarHouseCrawl/picture/b1.png" width="800">

