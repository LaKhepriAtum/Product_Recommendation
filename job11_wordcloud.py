import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
import matplotlib as mpl
import numpy as np
from PIL import Image

fontpath = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=fontpath).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

df = pd.read_csv('./crawling_data(drink)/drink_onesentence.csv')
print(df.head())

words = df.iloc[105, 1]
print(words)

words = words.split()
print(words)

worddict_1 = collections.Counter(words)
worddict_1 = dict(worddict_1)
worddict_1 = dict(sorted(worddict_1.items(),
                    key=lambda item:item[1],
                      reverse=True))
print(worddict_1)

words = df.iloc[11, 1]
# print(words)

words = words.split()
# print(words)

worddict_2 = collections.Counter(words)
worddict_2 = dict(worddict_2)
worddict_2 = dict(sorted(worddict_2.items(),
                    key=lambda item:item[1],
                      reverse=True))
print(worddict_2)
wordcloud_img_1 = WordCloud(
    background_color='white', max_words=500,
    font_path=fontpath).generate_from_frequencies(worddict_1)

wordcloud_img_2 = WordCloud(
    background_color='white', max_words=500,
    font_path=fontpath).generate_from_frequencies(worddict_2)



plt.figure(figsize=(12, 4))
plt.imshow(wordcloud_img_1, interpolation='bilinear')
plt.axis('off')

plt.figure(figsize=(12, 4))
plt.imshow(wordcloud_img_2, interpolation='bilinear')
plt.axis('off')
plt.show()