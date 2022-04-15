import pandas as pd

df = pd.read_csv('./crawling_data/snack_cleaned_data_02.csv')
df.dropna(inplace=True) # null 값 제거
print(df.head())
df.info()
print(df.head())
print(df.duplicated().sum())
df.drop_duplicates(inplace= True) # 중복 제거
df.info()

one_sentences = []
for product in df['product'].unique():
    temp = df[df['product'] == product] # title이 같은 거 찾기
    temp = temp['cleaned_sentences']
    one_sentence = ' '.join(temp) # 하나의 문장으로 합친다.
    one_sentences.append(one_sentence)
df_one_sentence = pd.DataFrame(
    {'product':df['product'].unique(), 'cleaned_sentences':one_sentences})
print(df_one_sentence.head())
df_one_sentence.dropna(inplace=True)
df_one_sentence.to_csv('./crawling_data/snack_onesentence.csv', index = False)