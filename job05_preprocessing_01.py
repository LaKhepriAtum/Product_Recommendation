import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/snack_crawling_data.csv')
print(df.head())
df.info()

# count = 0
# for i in range(len(df)):
#     if len(df.iloc[i, 1])> 1000: # i 번째 행의 1열이 1000 이상
#         count+=1
#         df.iloc[i, 1] = df.iloc[i, 1][:1000] # 천글자 이상을 짜르기
# print(count)

stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords_list = list(stopwords['stopword'])

cleaned_sentences = []
for review in df.review_list:
    review = re.sub('[^가-힇 ]', '', review) # 한글 + 띄어쓰기(차이가 크다)
    review_word = review.split(' ')
    words = []
    for word in review_word:
        if word not in stopwords_list:
            words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
df = df[['product', 'cleaned_sentences']]
df = df.drop_duplicates(['cleaned_sentences'], keep='first')
df.info()
df.to_csv('./crawling_data/snack_cleaned_data.csv', index = False)