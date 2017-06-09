# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2017/6/5 下午9:13
# # @Author  : Sylor_Huang
# # @File    : boss.py
# # @Software: PyCharm
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# browser = webdriver.Chrome()
# wait = WebDriverWait(browser, 10)
#
# def search():
#     try:
#         browser.get('http://www.zhipin.com/?sid=sem_pz_bdpc_index')
#         input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div.home-box > div.home-main > div.search-box > div.search-form > form > div.search-form-con > p > input")))
#         submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > div.home-box > div.home-main > div.search-box > div.search-form > form > button")))
#         input.send_keys('python')
#         submit.click()
#         time.sleep(5)
#     except TimeoutError:
#         print('超时连接')
#
#
# def next_page():
#     try:
#         count = 1
#
#         while count <= 30:
#             # soup = BeautifulSoup(html, 'lxml').select('#main > div.job-box > div.job-list > div.page > a.next')[0]
#             # next_page_link = str(soup).find('next')  # 需要把返回的值转换为str，然后用find搜索，判断是否存在指定字符串.此方法无法判断最后一页，没想明白
#             html = browser.page_source  #获取网页源代码
#             soup = BeautifulSoup(html,'lxml').select('#main > div.job-box > div.job-list > ul > li')
#             for items in soup:
#                 href = 'http://www.zhipin.com' + items.a.attrs['href']  #转化为完整路径，urljoin只在scrapy中引用response才能自动转。
#                 parse_html(href)
#             next_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#main > div.job-box > div.job-list > div.page > a.next')))
#             print('正在翻页到第'+ str(count) +'页')
#             next_link.click()
#             time.sleep(5)
#             count = count + 1
#         else:
#             print('已到最后一页')
#     except:
#         print('链接出现错误')
#
#
# def parse_html(html):
#     html_a = browser.page_source
#     html_parse = BeautifulSoup(html_a,'lxml')
#     data = {
#         'work':html_parse.find('#main > div.job-banner > div > div > div.info-primary > div.name').text(),
#         'company':html_parse.find('#main > div.job-banner > div > div > div.info-company > h3').text()
#     }
#     print(data)
#
#
# def main():
#     search()
#     next_page()
#
#
#
# if __name__ == '__main__':
#     main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/5 下午9:13
# @Author  : Sylor_Huang
# @File    : boss.py
# @Software: PyCharm
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from bosszhipin.config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400,900)
wait = WebDriverWait(browser, 10)

def search():
    try:
        browser.get('http://www.zhipin.com/?sid=sem_pz_bdpc_index')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div.home-box > div.home-main > div.search-box > div.search-form > form > div.search-form-con > p > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > div.home-box > div.home-main > div.search-box > div.search-form > form > button")))
        input.send_keys(KEYWORD)
        submit.click()
        time.sleep(5)
    except TimeoutError:
        print('超时连接')


def next_page():
    try:
        count = 1

        while count <= 30:
            print('当前是第'+ str(count) +'页')
            print('正在获取职位信息')
            parse_html()
            # soup = BeautifulSoup(html, 'lxml').select('#main > div.job-box > div.job-list > div.page > a.next')[0]
            # next_page_link = str(soup).find('next')  # 需要把返回的值转换为str，然后用find搜索，判断是否存在指定字符串.此方法无法判断最后一页，没想明白
            next_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#main > div.job-box > div.job-list > div.page > a.next')))
            print('正在翻页到第'+ str(count+1) +'页')
            next_link.click()
            time.sleep(5)
            count = count + 1
        else:
            print('已到最后一页')
    except ConnectionError:
        print('链接出现错误')


def parse_html():
    try:
        html = browser.page_source
        soup = BeautifulSoup(html,'lxml').select('#main .job-box .job-list ul li')
        url_origin = 'http://www.zhipin.com'
        for item in soup:
            href = url_origin + item.a.attrs['href']
            browser.get(href)   #浏览器打开href
            total_html = browser.page_source   #获得href页面的源代码，并且是txt格式的。
            soup_html = BeautifulSoup(total_html,'lxml')
            info_company = soup_html.select('#main > div.job-banner > div.inner > div.job-primary > div.info-company > p')
            company = info_company[0].get_text()
            company_profile = info_company[1].get_text(separator=u' ')
            time = soup_html.select('#main > div.job-banner > div > div > div.info-primary > div.job-author > span')[0].get_text()
            work  = soup_html.select('#main > div.job-banner > div > div > div.info-primary > div.name')[0].get_text(separator=u' ')
            experience = soup_html.select('#main > div.job-banner > div > div > div.info-primary > p')[0].get_text(separator=u' ')
            work_profile = soup_html.select('#main > div.job-box > div > div.job-detail > div.detail-content > div.job-sec > div.text')[0].get_text().strip()
            location = soup_html.select('#main > div.job-box > div > div.job-detail > div.detail-content > div.job-sec > div > div.location-address')[0].get_text()
            data = {
                'company':company,
                'company_profile':company_profile,
                'time':time,
                'work':work,
                'experience':experience,
                'work_profile':work_profile,
                'location':location
            }

            save_to_mongodb(data)
            browser.back()


    except TimeoutError:
        print('获取职位错误')

def save_to_mongodb(data):
    try:
        if db[MONGO_TABLE].insert(data):
            print('存储到MONGODB成功')
    except Exception:
        print('存储到MONGODB失败')


def main():
    search()
    next_page()



if __name__ == '__main__':
    main()

    # main > div.job-banner > div > div > div.info-company > p:nth-child(3)