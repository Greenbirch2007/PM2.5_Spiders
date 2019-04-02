#! -*- coding:utf-8 -*-

# 与当日天气的相关性　爬天气数据
import datetime
import re
import time
from requests.exceptions import RequestException
import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()

def get_one_page(url):

    driver.get(url)
    html = driver.page_source
    return html




# 数据解析有了重复项！
def parse_oneDay(html):
    oneDay_contents = []


    selector = etree.HTML(html)

    dtime = selector.xpath('//*[@id="content"]/div[3]/table/tbody/tr/td[1]/text()')
    AQI = selector.xpath('//*[@id="content"]/div[3]/table/tbody/tr/td[3]/text()')
    levels = selector.xpath('//*[@id="content"]/div[3]/table/tbody/tr/td[2]/text()')
    pm25 = selector.xpath('//*[@id="content"]/div[3]/table/tbody/tr/td[5]/text()')
    # 解析很费时间，想法是先把数据结构整理好，然后一次性的清洗


    for i1,i2,i3,i4 in zip(dtime[1:],AQI[1:],levels[1:],pm25[1:]):
        ha_list = []
        ha_list.append([i1,i2,i3,i4])
        for item in ha_list:
            f4 = []
            for it in item:
                wt = ''.join(it.split())
                f4.append(wt)
            f4_tuple = tuple(f4)
            oneDay_contents.append(f4_tuple)


    return oneDay_contents





def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='PM25',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(67,88):
        sql = 'select links from XA_links where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url = data['links']
        yield url



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='PM25',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into XA_OneDay (dtime,AQI,levels,pm25) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except :
        print('出列啦')



# 网站也不稳定，所以手动拼接来爬吧
#网络不好，也影响爬虫！

if __name__ == '__main__':
    for url_str in Python_sel_Mysql():
        time.sleep(2)

        html = get_one_page(url_str)
        time.sleep(2)

        contet = parse_oneDay(html)
        insertDB(contet)
        print(datetime.datetime.now())


# #
# create table XA_OneDay(
# id int not null primary key auto_increment,
# dtime varchar(10),
# AQI varchar(10),
# levels varchar(10),
# pm25 varchar(10)
# ) engine=InnoDB  charset=utf8;


#  drop  table XA_OneDay;







# b = ['\n                                        2019-03-01', '92\n                                       ', '\n                                       良', '67']
# w = []
# for item in b:
#
#     z = ''.join(item.split())
#     w.append(z)
# print(w)