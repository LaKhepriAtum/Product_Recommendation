import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec

df_reviews = pd.read_csv('crawling_data/drink_onesentence.csv')
df_reviews.info()
def getRecommendation(cosine_sim, input_drink):
    simScore = list(enumerate(cosine_sim[-1]))
    # print(len(simScore))
    # print(simScore)
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    print(simScore)
    drknkidx = [i[0] for i in simScore]
    print(drknkidx)
    recMovieList = df_reviews.iloc[drknkidx]
    input_drink = input_drink.split()
    print(input_drink)
    # for i in len(input_drink):
    recMovieList = recMovieList[(~recMovieList['product'].str.contains(input_drink[0])) & (~recMovieList['product'].str.contains(input_drink[1]))]
    print(recMovieList)
    return recMovieList.iloc[:10, 0]

Tfidf_matrix = mmread('./models/drink.mtx').tocsr()
with open('./models/drink.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 영화 제목 이용
# input_drink = '시그너스 토닉워터'
# drink_idx = df_reviews[df_reviews['product'] ==input_drink].index[0] #df_reviews['title'] =='기생충'조건 .index[0]->title, .index[1]-> cleaned_sentences
# print(drink_idx)
# cosine_sim = linear_kernel(Tfidf_matrix[drink_idx],
#                            Tfidf_matrix)
# recommendation_titles = getRecommendation(cosine_sim, input_drink)
# print(recommendation_titles)

# # 영화 index이용
drink_idx = 218
print(df_reviews.iloc[drink_idx, 0]) # movie_idx 조건의 o 번째 col df.iloc[행, 열]
# cos 가 1에 가깝다 = 유사한 문장이다. , -1에 가깝다 = 반대다, 0에 가깝다 = 유사성X

cosine_sim = linear_kernel(Tfidf_matrix[drink_idx], Tfidf_matrix) # 1에 가까우면 유사하다.Tfidf_matrix[movie_idx]관심영화 ,  Tfidf_matrix나머지 모든 영화
# 의 cosine 유사도를 준다, len->Tfidf_matrix의 갯수, 2중 리스트
print(cosine_sim)
recommendation = getRecommendation(cosine_sim)
print(recommendation)

# key_word 이용
# embedding_model = Word2Vec.load('./models/word2vexModel.model')
# key_word = ''
# sim_word = embedding_model.wv.most_similar(key_word, topn=10) # key_word와 가장 큰 유사도를 보여주는 10개 가져오기
# sentence = [key_word] * 11
# words = []
# for word, _ in sim_word:
#     words.append(word)
# for i, word in enumerate(words):
#     sentence += [word] * (10 - i) # 유사도가 큰 순서대로 가중치를 부여
#
# sentence = ' '.join(sentence)
# sentence = '적화통일돼서 배에서 기생충 키우고 싶나? 뭔 북한넘들 미화 영화가 이렇게 많냐.배우들도 생각이 있으면 이런 영화는 걸러야하는 거 아니냐.박정희, 전두환 군부 독재 시절을 미화하는 영화에 출연하면 무식해보이 듯이,이런 북한 미화 영화 출연하는 것도 참으로 정신나간 듯이 보인다.제목도 강철비가 뭐냐. 김영환 강철서신에서 가져온거냐.정말 적당히 하자.'
# sentence_vec = Tfidf.transform([sentence]) #pickle 로 백터값 만들기
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix) # 백터값들과 영화의 백서값으로 새로운 유사도 찾기
#
# # cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation_titles)