from gensim.models import Word2Vec
import pandas as pd

review_word = pd.read_csv('./crawling_data/snack_onesentence.csv')
review_word.info()

cleaned_token_review = list(review_word['cleaned_sentences']) # dataFrame의 cleaned_sentences만 리스트로
print(cleaned_token_review[0])
cleaned_tokens = []# 토큰 단위로 짜르기
for sentence in cleaned_token_review:
    token = sentence.split() # 디폴트 -> 띄어쓰기 token 단위로 짜르기
    cleaned_tokens.append(token)
print(cleaned_tokens[0]) # 토큰 단위로 짤라진 list

embedding_model = Word2Vec(cleaned_tokens, vector_size = 100, #vector_size-> 차원을 축소할 차원크기
                           window = 4, min_count=20, # window 몇개의 형태소로 해당하는 단어의 성질,
                           # 특징을 파악할 것인가? 형태소의 list에서 4개씩 짤라서 학습, conv의 kernel과 비슷,
                           # 일반적으로 4개 min_count->전체의 단어 중 사용의 빈도가 20번은 나와야 백터화
                           workers = 4, epochs = 100, sg = 1) #workers-> 컴퓨터 core(cpu) 갯수를 몇개 사용해야 하는가?, epochs 몇번 학습할 것인가
                            # sg 0->CBOW(back of word-> 단어가 , 1->Skip-gram 인배딩할 때의 알고리즘
# embedding_model, 빈도수가 20개 넘는 단어들의 100차원 좌표값
embedding_model.save('./models/snack_word2vexModel.model')
print(embedding_model.wv.index_to_key)
print(len(embedding_model.wv.index_to_key))