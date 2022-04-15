from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


df = pd.read_csv('./crawling_data/product_name.csv')
stopwords = pd.read_csv('./crawling_data/stopwords_drink.csv')
stopwords_list = list(stopwords['stopword'])
cleaned_names = []
for name in df.product_name:
    name = re.sub('[^가-힣 ]', '', name)
    new_name = name.split(' ')

    new_names = []
    for name in new_name:
        if len(name) > 1:
            if name not in stopwords_list:
                new_names.append(name)
    cleaned_name = ' '.join(new_names)
    cleaned_names.append(cleaned_name)
df['product_name'] = cleaned_names
df = df[['product_name']]
df.drop_duplicates(inplace=True)
df.to_csv('./crawling_data/cleaned_product_name.csv', index=False)
df.info()