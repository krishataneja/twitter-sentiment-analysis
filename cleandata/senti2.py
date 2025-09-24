import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("work_cleaned.csv")
analyzer = SentimentIntensityAnalyzer()

def get_score(text):
    scores = analyzer.polarity_scores(str(text))
    return pd.Series({
        "negative": scores["neg"],
        "neutral": scores["neu"],
        "positive": scores["pos"],
        "compound": scores["compound"]
    })
sentiment_scores = df["clean_text"].apply(get_score)
df = pd.concat([df, sentiment_scores], axis=1) #axis = 1 for columns

def classify_sent(compound):
    if compound >= 0.1:
        return "positive"
    elif compound <= -0.1:
        return "negative"
    else:
        return "neutral"

df["sentiment"] = df["compound"].apply(classify_sent)
df.to_csv("work_sentiment4.csv", index=False)
print("done")
