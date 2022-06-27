import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE # 차원 축소
from matplotlib import font_manager, rc
import matplotlib as mpl

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname = font_path).get_name() # 파일 이름은 이렇게 생겼는데 안에 폰트 이름이 있다.

# !apt -qq -y install fonts-nanum
# import matplotlib as mpl
# import matplotlib.font_manager as fm
# fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
# font = fm.FontProperties(fname=fontpath, size=9)
# plt.rc('font', family='NanumBarunGothic')
# mpl.font_manager._rebuild() #colab에서 실행할 때 필요한 것

mpl.rcParams['axes.unicode_minus']=False # y축 - 있을 때 안 깨지게
rc('font', family = font_name)# 폰트 mat에 적용

embedding_model = Word2Vec.load('./models/freeze_word2vexModel.model')
print(embedding_model.wv.index_to_key) # dict의 key는 단어 이름, vocab의 키 보기
print(len(embedding_model.wv.index_to_key)) # 최소 20번 이상 나오는 단어의 개수

key_word = '혼밥'


sim_word = embedding_model.wv.most_similar(key_word, topn = 20)# 여름 근처에 있는 단어
print(sim_word)

vectors = []
labels = []
for label, _ in sim_word: # sim_word 에서 2개의 값을 반환하는데 안 사용할 유사도는 _로 받는다.
    labels.append(label)
    vectors.append(embedding_model.wv[label]) #wv->word vector
df_vectors = pd.DataFrame(vectors) # 100개 차원의 좌표값(벡터)
print(df_vectors.head())

tsne_model = TSNE(perplexity=40, n_components=2,
                  init='pca', n_iter=2500)
new_value =tsne_model.fit_transform(df_vectors)# 100 개의 차원을 2개의 좌표값으로 fit_transform
df_xy = pd.DataFrame({'word':labels, 'x':new_value[:,0], 'y':new_value[:,1]}) #0번째 col을 x, 1번째 col을 y
print(df_xy)
print(df_xy.shape) # row,col
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)

plt.figure(figsize=(8,8))
plt.scatter(0,0, s= 1500, marker= '*') # 원점에 1500 size의 별 그리기
for i in range(len(df_xy.x) - 1):
    a = df_xy.loc[[i, (len(df_xy) - 1)], :] # 첫번째 자료의 x의 길이(10)개 -1, (len(df_xy) - 1)-> keyword 단어올라프
    plt.plot(a.x, a.y, '-D', linewidth = 1) # 각각의 단어의 좌표와 keyword의 좌표를 선으로 이어준다.
    plt.annotate(df_xy.word[i], xytext = (1, 1),# 단어 글씨 써주기 시작 , 위로 1 좌로 1
                 xy = (df_xy.x[i], df_xy.y[i]), # x, y의 좌표
                 textcoords = 'offset points',
                 ha='right', va = 'bottom')# 단어 글씨 써주기 끝 , 오른쪽 정렬, 아래 정렬
plt.show()

# TF(text frequency),한문장 안에서의 빈도 ->*, DF(document frequency)문서 안의 빈도-> 별로 도문이 많이 되지 않는다.->-