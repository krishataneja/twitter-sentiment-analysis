import pandas as pd
from transformers import pipeline
import torch
from sklearn.metrics import classification_report

# STEP 1: Load the CSV
df = pd.read_csv("EDA1clean.csv")
print("Loaded", len(df), "tweets.")

# STEP 2: Load DistilBERT pipeline
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english",
                      device=device)

# STEP 3: Apply in batches
def get_sentiments(clean_text):
    results = classifier(clean_text)
    return [r['label'].lower() for r in results]

batch_size = 32
sentiments = []

print("Running sentiment analysis...")
for i in range(0, len(df), batch_size):
    batch = df['clean_text'].iloc[i:i+batch_size].tolist()
    sentiments.extend(get_sentiments(batch))
    print(f"Processed {i+len(batch)}/{len(df)} tweets")

df['transformer_sentiment'] = sentiments

'''# STEP 4: Compare to VADER if available
if 'vader_sentiment' in df.columns:
    print("\nClassification report comparing VADER vs Transformer:")
    print(classification_report(df['vader_sentiment'], df['transformer_sentiment']))
else:
    print("\nVADER sentiment not found. Just added transformer results.")'''

# STEP 5: Save results
df.to_csv("filextrans.csv", index=False)
print("\nSaved to filextrans.csv ✅")
