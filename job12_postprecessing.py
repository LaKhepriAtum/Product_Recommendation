import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_data_02.csv')
df.dropna(inplace=True)
print(df.head())
df.info()

stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords_list = list(stopwords['stopword'])
cleaned_sentences = []
stopwords_movie = ['개수', '박스']
stopwords_list = stopwords_list + stopwords_movie
for review in df.cleaned_sentences:
    review_word = review.split(' ')

    words = []
    for word in review_word:
        if len(word) > 1:
            if word not in stopwords_list:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
df.dropna(inplace=True)
df.to_csv('./crawling_data/cleaned_data_02.csv',
          index=False)
df.info()
print('end')