import pandas as pd
from deep_translator import GoogleTranslator
import time

# Load the dataset
df = pd.read_csv("LGprojectdata.csv", encoding="utf-8")

# Add empty column if not already present
if 'translated_text' not in df.columns:
    df['translated_text'] = ""

# Translate in batches with retry
BATCH_SIZE = 50
translator = GoogleTranslator(source='auto', target='en')

for start in range(0, len(df), BATCH_SIZE):
    end = start + BATCH_SIZE
    batch = df.iloc[start:end]

    texts_to_translate = []
    indexes = []

    for idx, row in batch.iterrows():
        text = str(row['text'])
        if not text.strip():
            df.at[idx, 'translated_text'] = ''
        elif not row['translated_text']:  # only translate if not already translated
            texts_to_translate.append(text)
            indexes.append(idx)

    if texts_to_translate:
        try:
            translations = translator.translate_batch(texts_to_translate)
            for idx, translated in zip(indexes, translations):
                df.at[idx, 'translated_text'] = translated
            print(f"✅ Translated rows {start} to {end}")
        except Exception as e:
            print(f"❌ Error at rows {start}-{end}: {e}")
            print("⏳ Waiting 10 seconds and retrying...")
            time.sleep(10)
            continue  # Skip to next batch after waiting

    time.sleep(1)  # brief pause to stay under rate limit

# Save progress
df.to_csv("translated_tweets.csv", index=False, encoding="utf-8")
print("✅ All done! Translations saved to translated_tweets.csv")
