import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from tensorflow.keras.models import load_model
from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib import request
from PIL import Image
import numpy as np
import random
import webbrowser
import glob

form_window = uic.loadUiType('./product_app.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.product_lbl.setText("JNK's Choice")
        self.product_box.addItems(['카테고리를 선택하세요'])
        # self.product_box.clear()
        self.data_paths = [glob.glob('./models/*')[0:4],glob.glob('./models/*')[4:8],glob.glob('./models/*')[8:12],glob.glob('./models/*')[12:16],glob.glob('./models/*')[16:20],glob.glob('./models/*')[20:44]]
        self.product = ['카테고리','음료','냉동식품', '건강식품','가공식품','과자', '커피, 차']
        self.pixmap = QPixmap()
        self.pixmap2 = QPixmap()
        self.pixmap3 = QPixmap()
        for i in self.product:
            self.category_box.addItem(i)
        self.category_box.currentIndexChanged.connect(self.category_box_slot)
        self.product_box.currentIndexChanged.connect(self.product_box_slot)
        self.btn_recommend.clicked.connect(self.btn_recommend_slot)


    def btn_recommend_slot(self):
        sentence = self.le_keyword.text()
        input_words = sentence.split()
        if len(input_words) >= 5:
            sentence_vec = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)

            recommendation_titles = self.recommend_by_sentence(sentence)
            recommendation_titles = recommendation_titles.tolist()
            self.label4(recommendation_titles[0])
            self.label5(recommendation_titles[1])
            self.label6(recommendation_titles[2])

        else:
            key_word = input_words[0]


            try:
                sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
            except:
                self.product_lbl.setText('카테고리 설정을 바꿔 보세요')
                return
            sentence = [key_word] * 11
            words = []
            for word, _ in sim_word:
                words.append(word)
            for i, word in enumerate(words):
                sentence += [word] * (10 - i)
            sentence = ' '.join(sentence)
            recommendation_titles = self.recommend_by_sentence(sentence)
            recommendation_titles = recommendation_titles.tolist()
            self.label4(recommendation_titles[0])
            self.label5(recommendation_titles[1])
            self.label6(recommendation_titles[2])
            # self.lbl_recommend.setText(recommendation_titles)

    def recommend_by_sentence(self, sentence):
        print(sentence)
        sentence_vec = self.Tfidf.transform([sentence])
        print(sentence_vec)
        cosin_sim = linear_kernel(sentence_vec,
                                  self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosin_sim)
        print(recommendation_titles)
        return recommendation_titles


    def product_box_slot(self):
        product = self.product_box.currentText()
        self.product_lbl.setText(product[18:])
        recommendation_titles = self.recommend_by_product_title(product)
        recommendation_titles_list= recommendation_titles.tolist()
        print(recommendation_titles_list)
        self.label4(recommendation_titles_list[0])
        self.label5(recommendation_titles_list[1])
        self.label6(recommendation_titles_list[2])

    def recommend_by_product_title(self, product):
        movie_idx = self.df_reviews[self.df_reviews['product'] == product].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosine_sim)
        print(type(recommendation_titles))
        return recommendation_titles[:3]

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[1:11]
        movieidx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieidx]
        return recMovieList.iloc[:, 0]


    def category_box_slot(self):
        category = self.category_box.currentText()
        i = 1
        idx = 0
        for path in self.data_paths:
            print(path)
            print(category)
            if category == self.product[i]:
                name = path[2]
                print('debug')
                self.df_reviews = pd.read_csv(name)
                print('debug')
                self.embedding_model = Word2Vec.load(path[idx+3])
                self.Tfidf_matrix = mmread(path[idx]).tocsr()
                with open(path[idx+1], 'rb') as f:
                    self.Tfidf = pickle.load(f)
            print(i)
            i += 1

        self.pro_list = list(self.df_reviews['product'])
        print(self.pro_list)
        # self.product_box.clear()
        # print('debug')
        self.product_box.addItems(self.pro_list)

        self.product_lbl.setText(category)
        self.rand = random.randint(0, len(self.pro_list))
        self.label1(self.rand)
        self.rand2 = random.randint(0, len(self.pro_list))
        self.label2(self.rand2)
        self.rand3 = random.randint(0, len(self.pro_list))
        self.label3(self.rand3)



    def label1(self, a):
        product_url, img, product_name = self.product_search(a)
        self.pixmap.loadFromData(img)
        self.img_lbl_1.setPixmap(self.pixmap.scaledToHeight(230))
        print(product_name)
        self.prod_lbl_1.setText(product_name)
        self.buy_btn_1.setText('구매하기')
        self.buy_btn_1.clicked.connect(lambda: webbrowser.open('https://www.coupang.com/' + product_url))

    def label2(self, b):
        product_url2, img2, product_name2 = self.product_search(b)
        self.pixmap2.loadFromData(img2)
        self.img_lbl_2.setPixmap(self.pixmap2.scaledToHeight(230))
        print(product_name2)
        self.prod_lbl_2.setText(product_name2)
        self.buy_btn_2.setText('구매하기')
        self.buy_btn_2.clicked.connect(lambda: webbrowser.open('https://www.coupang.com/' + product_url2))

    def label3(self, a):
        self.rand = random.randint(0, len(self.pro_list))
        product_url3, img3, product_name3 = self.product_search(a)
        self.pixmap3.loadFromData(img3)
        self.img_lbl_3.setPixmap(self.pixmap3.scaledToHeight(230))
        print(product_name3)
        self.prod_lbl_3.setText(product_name3)
        self.buy_btn_3.setText('구매하기')
        self.buy_btn_3.clicked.connect(lambda: webbrowser.open('https://www.coupang.com/' + product_url3))

    def label4(self, a):
        product_url, img, product_name = self.product_search2(a)
        self.pixmap.loadFromData(img)
        self.img_lbl_1.setPixmap(self.pixmap.scaledToHeight(230))
        print(product_name)
        self.prod_lbl_1.setText(product_name)
        self.buy_btn_1.setText('구매하기')
        self.buy_btn_1.clicked.connect(lambda: webbrowser.open('https://www.coupang.com/' + product_url))

    def label5(self, b):
        product_url2, img2, product_name2 = self.product_search2(b)
        self.pixmap2.loadFromData(img2)
        self.img_lbl_2.setPixmap(self.pixmap2.scaledToHeight(230))
        print(product_name2)
        self.prod_lbl_2.setText(product_name2)
        self.buy_btn_2.setText('구매하기')
        self.buy_btn_2.clicked.connect(lambda: webbrowser.open('https://www.coupang.com/' + product_url2))

    def label6(self, a):
        self.rand = random.randint(0, len(self.pro_list))
        product_url3, img3, product_name3 = self.product_search2(a)
        self.pixmap3.loadFromData(img3)
        self.img_lbl_3.setPixmap(self.pixmap3.scaledToHeight(230))
        print(product_name3)
        self.prod_lbl_3.setText(product_name3)
        self.buy_btn_3.setText('구매하기')
        self.buy_btn_3.clicked.connect(lambda: webbrowser.open('https://www.coupang.com/' + product_url3))


    def product_search(self, num):
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        # url = f'https://www.coupang.com/np/search?q={self.pro_list[num]}&channel=recent'
        # try:
        #     res = requests.get(url, headers=headers, timeout=3)
        # except:
        #     print('error')
        #     # self.warning_word.setText('인터넷 접속이 불안정합니다!!\n다시 접속해 주세요 ')
        #     return
        # print('debug01')
        # soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)
        # img_url = soup.find("img", {"class": "search-product-wrap-img"})['src']
        # print('debug03')
        # product_url = soup.find('a', {'class': 'search-product-link'})['href']
        # print('debug04')
        # product_name = soup.find('div', {'class': 'name'}).get_text()
        img_url = 'thumbnail6.coupangcdn.com/thumbnails/remote/492x492ex/image/retail/images/2020/04/28/11/5/0fa77540-d4d2-4b73-8236-256c1874911f.jpg'
        product_url = 'vp/products/1519330646?itemId=2607093811&vendorItemId=70598215704&sourceType=CATEGORY&categoryId=225361&isAddedCart='
        product_name = '햇살닭 저염훈제닭가슴살 플러스 (냉동)'
        URL = 'https://'+img_url
        print(URL)
        img = urllib.request.urlopen(URL).read()
        print('debug01')
        return product_url, img, product_name

    def product_search2(self, a):
        print('product_search2')
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        # self.rand = random.randint(0, len(self.pro_list))
        # url = f'https://www.coupang.com/np/search?q={a}&channel=recent'
        # print(url)
        # try:
        #     res = requests.get(url, headers=headers, timeout=3)
        # except:
        #     print('error')
        #     # self.warning_word.setText('인터넷 접속이 불안정합니다!!\n다시 접속해 주세요 ')
        #     return
        # soup = BeautifulSoup(res.text, 'html.parser')
        # img_url = soup.find("img", {"class": "search-product-wrap-img"})['src']
        # product_url = soup.find('a', {'class': 'search-product-link'})['href']
        # product_name = soup.find('div', {'class': 'name'}).get_text()
        img_url = 'thumbnail6.coupangcdn.com/thumbnails/remote/492x492ex/image/retail/images/2020/04/28/11/5/0fa77540-d4d2-4b73-8236-256c1874911f.jpg'
        product_url = 'vp/products/1519330646?itemId=2607093811&vendorItemId=70598215704&sourceType=CATEGORY&categoryId=225361&isAddedCart='
        product_name = '햇살닭 저염훈제닭가슴살 플러스 (냉동)'
        URL = 'https://'+img_url
        img = urllib.request.urlopen(URL).read()
        print(product_name)
        return product_url, img, product_name


    def delete(self):
        # delete items of list
        self.product_box.clear()
        self.product_box.addItems(self.pro_list)



app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())