import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/snack_cleaned_data.csv')  # 파일 열기
df.dropna(inplace=True) # null 값 제거
print(df.head())
df.info()
print(df.isnull().sum()) # null 값의 개수의 합

okt = Okt()
count = 0
cleaned_sentences = []
for sentence in df.cleaned_sentences:
    count += 1
    if count % 10 ==0:
        print('.', end='')
    if count % 100 == 0:
        print()
    token = okt.pos(sentence, stem=True) # 품사를 기준으로 나눈다. list 안의 dict 형태로
    # print(token)
    df_token = pd.DataFrame(token,  columns=['word', 'class']) # 단어, 품사
    df_token = df_token[(df_token['class']=='Noun') | # 명사인 단어
                                (df_token['class']=='Verb') | # 동사
                                (df_token['class']=='Adjective')]
    cleaned_sentence = ' '.join(df_token.word) # 띄어쓰기를 기준으로 합친다.
    # print(cleaned_sentence)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
print(df.head())
df.info()
df.to_csv('./crawling_data/snack_cleaned_data_02.csv', index = False)