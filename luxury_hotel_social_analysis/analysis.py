import pandas as pd

# load data
df = pd.read_csv("hotel_posts_clean.csv")

# quick sanity check
print(df.head())
print(df.columns)
print(len(df))

def extract_hashtags(text):
    if pd.isna(text):
        return []
    return [tag.lower() for tag in text.split()]

df["hashtag_list"] = df["hashtags"].apply(extract_hashtags)

# convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# extract year and month
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month

def extract_hashtags(text):
    if pd.isna(text):
        return []
    return [tag.lower() for tag in text.split()]

df["hashtag_list"] = df["hashtags"].apply(extract_hashtags)

from collections import Counter

all_hashtags = Counter(
    tag for tags in df["hashtag_list"] for tag in tags
)

top_hashtags = all_hashtags.most_common(15)

print("Top 15 hashtags:")
for tag, count in top_hashtags:
    print(tag, count)

import matplotlib.pyplot as plt

tags, counts = zip(*top_hashtags)

plt.figure(figsize=(8, 6))
plt.barh(tags[::-1], counts[::-1])
plt.title("Most Common Hashtags Used by Luxury Hotels")
plt.xlabel("Frequency")
plt.ylabel("Hashtag")
plt.tight_layout()
plt.show()

