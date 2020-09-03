import requests
import time
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@3.35.10.2', 27017)
client = MongoClient('localhost', 27017)
db = client.dbmyproject

total_gu = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구",
            "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구", "분당구", "중원구", "수정구", "수지구", "기흥구", "처인구"]


def get_matjip_list(keyword):
    driver = webdriver.Chrome('/Users/jongcasso/Downloads/chromedriver')
    driver.implicitly_wait(2)
    driver.get('https://www.diningcode.com/')
    driver.find_element_by_xpath('//*[@id="div_popup"]/div/div[3]').click()
    time.sleep(2)
    driver.find_element_by_id('txt_keyword').send_keys(f'{keyword}')
    driver.find_element_by_xpath('//*[@id="txt_keyword"]').click()
    driver.find_element_by_id('txt_keyword').send_keys(Keys.RETURN)
    driver.find_element_by_xpath('//*[@id="btn_normal_list"]/a/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click()

    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    restaurants = soup.select('#div_list > li')

    for restaurant in restaurants:
        restaurant_name = restaurant.select_one('a > span.btxt')
        # print(restaurant_name)
        restaurant_type = restaurant.select_one('a > span.stxt')
        # print(restaurant_type)
        restaurant_tag = restaurant.select_one('a > span:nth-child(4).ctxt')
        # print(restaurant_tag)
        restaurant_local = restaurant.select_one('a >span > i.loca')
        # print(restaurant_local)
        restaurant_addr = restaurant.select_one('a >span:nth-child(5)')
        # print(restaurant_addr)
        if restaurant_name is not None:
            if restaurant_type is not None:
                if restaurant_tag is not None:
                    if restaurant_local is not None:
                        # print(restaurant_name.text, restaurant_type.text, restaurant_tag.text, restaurant_local.text,
                        #       restaurant_addr.contents[1])
                        doc = {
                            'name': restaurant_name.text,
                            'type': restaurant_type.text,
                            'tag': restaurant_tag.text,
                            'local': restaurant_local.text,
                            'addr': restaurant_addr.contents[1],
                            'gu': f'{keyword}'
                        }
                        db.matjip.insert_one(doc)

for gu in total_gu:
    keyword = f'{gu}'
    matjip_list = get_matjip_list(keyword)

    print(gu + " 크롤링 성공")
