import pandas as pd
import re

df = pd.read_csv("work.csv")  # make sure your file has a column like 'text' or 'tweet'
df = df.dropna(subset=["text"])    # drop empty rows
df = df.drop_duplicates(subset=["text"])  # keep only unique tweets

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)   # URLs
    text = re.sub(r'@\w+|#\w+', '', text)                 # mentions & hashtags
    text = re.sub(r'[^A-Za-z\s]', '', text)               # non-letter characters
    text = re.sub(r'\b(rt|amp)\b', '', text, flags=re.IGNORECASE)  # twitter noise
    text = re.sub(r'\s+', ' ', text).strip()              # extra spaces
    return text.lower()
df["clean_text"] = df["text"].apply(clean_text)

df["clean_text"] = df["clean_text"].str.replace(
    r"\blg india\b|\belectronics india\b|\blg electronics\b|\blg\b|\blgelelectronics\b|\blg product\b|\bindia\b",
    "",
    regex=True
)
df["clean_text"] = df["clean_text"].str.replace(r"\s+", " ", regex=True).str.strip()

df["word_count"] = df["clean_text"].apply(lambda x: len(x.split()))
df = df[df["word_count"] >= 3]
df.to_csv("work_cleaned.csv", index=False) 
print("number of rows after cleaning:", len(df))