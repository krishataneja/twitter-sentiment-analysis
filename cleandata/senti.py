import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("work_cleaned.csv")

analyzer = SentimentIntensityAnalyzer()

def classify_sent(text):
    scores = analyzer.polarity_scores(str(text))
    compound = scores["compound"]
    
    if compound >= 0.1:
        return "positive"
    elif compound <= -0.1:
        return "negative"
    else:
        return "neutral"

df["compound_score"] = df["clean_text"].apply(lambda x: analyzer.polarity_scores(str(x))["compound"])
df["sentiment"] = df["clean_text"].apply(classify_sent)

df.to_csv("work_sentiment3.csv", index=False)
print("done")
