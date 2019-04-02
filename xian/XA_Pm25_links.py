#! -*- coding:utf-8 -*-

# 与当日天气的相关性　爬天气数据
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

# driver = webdriver.Chrome()

def get_one_page(url):

    # driver.get(url)
    # html = driver.page_source
    # driver.quit()
    # return html
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except :
        return None


def parse_links(html):

    selector = etree.HTML(html)
    links = selector.xpath('//*[@id="bd"]/div[1]/div[3]/ul/li/a/@href')
    for item in links:
        links_list.append(("http://www.tianqihoubao.com"+item))


    return links_list












def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='PM25',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into XA_links (links) values (%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except :
        print('出列啦')





if __name__ == "__main__":
    links_list = []
    url = "http://www.tianqihoubao.com/aqi/xian.html"
    html = get_one_page(url)
    time.sleep(6)
    cont = parse_links(html)
    insertDB(cont)
#     for urls in cont:
#         oneDay_contents = []
#         html = get_one_page(urls)
#         contents = parse_oneDay(html)
#         print(contents)
    # insertDB(cont)


# create table XA_links(
# id int not null primary key auto_increment,
# links text
# ) engine=InnoDB  charset=utf8;


# drop  table XA_links;