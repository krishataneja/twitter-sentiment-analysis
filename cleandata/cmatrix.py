import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

df = pd.read_csv("combined_sentiments.csv")

print("Columns in dataset:", df.columns)

labels = ["positive", "neutral", "negative"]
cm = confusion_matrix(df['sentiment'], df['transformer_sentiment'], labels=labels)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap="Reds",
            xticklabels=labels,
            yticklabels=labels)


plt.xlabel("RoBERTa Sentiment")
plt.ylabel("VADER Sentiment")
plt.title("VADER vs RoBERTa Sentiment Analysis")
plt.tight_layout()
plt.show()
