import feedparser
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@3.35.10.2', 27017)
db = client.dbmyproject

url1 = "https://rss.blog.naver.com/mardukas"
url2 = "https://rss.blog.naver.com/bitterpan"
url3 = "https://rss.blog.naver.com/dodoti"
url4 = "https://rss.blog.naver.com/meal8030"


def crawl_blog1(url):
    d = feedparser.parse(url)
    # print( type(d) )
    # print( d.feed["title"] )
    db.blogpost1.delete_many({})
    for e in d.entries:
        # print("제목 = " + e.title)
        # print("내용 = " + e.description)
        # print("링크 = " + e.link)
        article = {'url': e.link, 'title': e.title, 'desc': e.description}
        db.blogpost1.insert_one(article)


def crawl_blog2(url):
    d = feedparser.parse(url)
    # print( type(d) )
    # print( d.feed["title"] )
    db.blogpost2.delete_many({})
    for e in d.entries:
        # print("2제목 = " + e.title)
        # print("2내용 = " + e.description)
        # print("2링크 = " + e.link)
        article = {'url': e.link, 'title': e.title, 'desc': e.description}
        db.blogpost2.insert_one(article)


def crawl_blog3(url):
    d = feedparser.parse(url)
    # print( type(d) )
    # print( d.feed["title"] )
    db.blogpost3.delete_many({})
    for e in d.entries:
        # print("3제목 = " + e.title)
        # print("3내용 = " + e.description)
        # print("3링크 = " + e.link)
        article = {'url': e.link, 'title': e.title, 'desc': e.description}
        db.blogpost3.insert_one(article)


def crawl_blog4(url):
    d = feedparser.parse(url)
    # print( type(d) )
    # print( d.feed["title"] )
    db.blogpost4.delete_many({})
    for e in d.entries:
        # print("4제목 = " + e.title)
        # print("4내용 = " + e.description)
        # print("4링크 = " + e.link)
        article = {'url': e.link, 'title': e.title, 'desc': e.description}
        db.blogpost4.insert_one(article)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/matjip', methods=['GET'])
def get_matjip():
    # gu_receive 라는 변수에 전달받은 구 이름을 저장합니다.
    gu_receive = request.args.get('gu_give')
    # print("gu_receive", gu_receive)
    # 구 이름에 해당하는 모든 맛집 목록을 불러옵니다.
    matjip_list = list(db.matjip.find({'gu': gu_receive}, {'_id': 0}))
    print(matjip_list)
    return jsonify({'result': 'success', 'matjip_list': matjip_list})


@app.route('/blogpost1', methods=['GET'])
def read_blogpost1():
    result = list(db.blogpost1.find({}, {'_id': 0}))
    # articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'articles': result})


@app.route('/blogpost2', methods=['GET'])
def read_blogpost2():
    result = list(db.blogpost2.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'articles': result})


@app.route('/blogpost3', methods=['GET'])
def read_blogpost3():
    result = list(db.blogpost3.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'articles': result})


@app.route('/blogpost4', methods=['GET'])
def read_blogpost4():
    result = list(db.blogpost4.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'articles': result})


if __name__ == '__main__':
    crawl_blog1(url1)
    crawl_blog2(url2)
    crawl_blog3(url3)
    crawl_blog4(url4)
    app.run('0.0.0.0', port=5000, debug=True)
