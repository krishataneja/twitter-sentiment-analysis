import pandas as pd
import re
from wordcloud import WordCloud
from collections import Counter
#from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

df = pd.read_csv("work_cleaned.csv", encoding="utf-8")
print(df.dtypes)  # datatypes
print(df.shape)  # dimensions
print(df.head())  # first 5 rows
print(df.describe(include='all'))  # basic stats
print(df.isnull().sum())  # missing values
for col in df.columns:
    print(col, len(df[col].unique()))  # unique values in each column
print(df.duplicated().sum())  # duplicate

# wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(width=800, height=400, background_color='black').generate(" ".join(df["clean_text"].dropna()))
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

from collections import Counter

all_words = " ".join(df["clean_text"].dropna()).split()
most_common = Counter(all_words).most_common(20)
print(most_common)


'''def remove_stopwords(text):
    return " ".join([word for word in text.split() if word.lower() not in ENGLISH_STOP_WORDS])

df["no_stopwords"] = df["clean_text"].apply(remove_stopwords)

# saving 
df.to_csv("removework.csv", index=False)
print("done")'''

#saving 
df.to_csv("EDA1clean.csv", index=False)
print("done")

