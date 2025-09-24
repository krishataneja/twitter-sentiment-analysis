#distilBERT: 
import pandas as pd
from transformers import pipeline
import torch
from sklearn.metrics import classification_report

# Load CSV (adjust filename if needed)
df = pd.read_csv("EDA1clean.csv")

# Load sentiment model
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english",
                      device=device)

# Run in batches
def get_sentiments(texts):
    results = classifier(texts)
    return [r['label'].lower() for r in results]

batch_size = 32
sentiments = []

for i in range(0, len(df), batch_size):
    batch = df['clean_text'].iloc[i:i+batch_size].tolist()
    sentiments.extend(get_sentiments(batch))
    print(f"Processed {i+len(batch)}/{len(df)}")

df['transformer_sentiment'] = sentiments

'''# Compare with VADER if available
if 'vader_sentiment' in df.columns:
    print("\nClassification Report (VADER vs Transformer):")
    print(classification_report(df['vader_sentiment'], df['transformer_sentiment']))'''

# Save results
df.to_csv("sentimentsoflife.csv", index=False)
print("\n✅ Done! File saved.")




#RobertBERTa: 
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import numpy as np

# Load tokenizer and model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

abels = ['negative', 'neutral', 'positive']

def get_sentiment(text):
    # Tokenize the tweet
    encoded_input = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(device)
    with torch.no_grad():
        output = model(**encoded_input)
    scores = output.logits[0].cpu().numpy()
    scores = np.exp(scores) / np.sum(np.exp(scores))  # Softmax
    predicted_label = labels[np.argmax(scores)]
    return predicted_label


# Load your CSV
df = pd.read_csv("EDA1clean.csv")

# Prepare an empty list to store predictions
predictions = []

# Loop through each tweet and print progress
total = len(df)
for i, text in enumerate(df['clean_text']):
    print(f"Processing tweet {i+1} of {total}")
    prediction = get_sentiment(text)
    predictions.append(prediction)

# Add predictions to the DataFrame
df['transformer_sentiment'] = predictions

# Save to CSV
df.to_csv("roberta_sentiment.csv", index=False)
print("✅ Done! File saved as roberta_sentiment.csv")


#combine 
import pandas as pd

# Load the VADER sentiment file
vader_df = pd.read_csv("work_sentiment3.csv")

# Load the RoBERTa transformer sentiment file
transformer_df = pd.read_csv("roberta_sentiment.csv")

# Merge them on the 'clean_text' column
merged = pd.merge(vader_df, transformer_df[['clean_text', 'transformer_sentiment']], on='clean_text', how='left')

# Save to a new CSV file
merged.to_csv("combined_sentiments.csv", index=False)
print("✅ Done! Combined file saved as combined_sentiments.csv")