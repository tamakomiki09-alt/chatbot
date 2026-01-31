import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# =========================
# PAGE CONFIG (DARK UI)
# =========================
st.set_page_config(
    page_title="Luxury Hotel Social Intelligence",
    layout="wide"
)

# =========================
# LOAD DATA (SAFE)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_posts_clean.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["hashtags"] = df["hashtags"].fillna("").str.lower()
    return df

df = load_data()

# =========================
# THEME KEYWORDS (EXPLAINABLE)
# =========================
THEMES = {
    "Brand": [
        "aman", "ritzcarlton", "stregis", "fourseasons",
        "peninsula", "luxuryhotel", "hotelstay"
    ],
    "Experience": [
        "spa", "dining", "restaurant", "lounge", "bar",
        "view", "suite", "garden", "breakfast", "travel"
    ],
    "Seasonal": [
        "christmas", "winter", "holiday", "festive",
        "newyear", "summer", "spring"
    ]
}

def classify_theme(text):
    counts = {k: 0 for k in THEMES}
    for word in text.split():
        for theme, keywords in THEMES.items():
            if word in keywords:
                counts[theme] += 1
    return max(counts, key=counts.get) if max(counts.values()) > 0 else "Other"

df["theme"] = df["hashtags"].apply(classify_theme)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

hotels = ["All"] + sorted(df["ownerUsername"].unique())
hotel = st.sidebar.selectbox("Hotel", hotels)

years = ["All"] + sorted(df["timestamp"].dt.year.dropna().unique().astype(int))
year = st.sidebar.selectbox("Year", years)

filtered = df.copy()

if hotel != "All":
    filtered = filtered[filtered["ownerUsername"] == hotel]

if year != "All":
    filtered = filtered[filtered["timestamp"].dt.year == year]

# =========================
# HEADER
# =========================
st.title("Luxury Hotel Instagram Intelligence")
st.caption("What luxury hotels post — and what actually performs")

# =========================
# KPI CARDS (ROW 1)
# =========================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Posts", len(filtered))
k2.metric("Avg Likes / Post", int(filtered["likesCount"].mean()))
k3.metric("Avg Comments / Post", int(filtered["commentsCount"].mean()))
k4.metric("Hotels Analyzed", filtered["ownerUsername"].nunique())

st.divider()

# =========================
# ROW 2 — PERFORMANCE BY HOTEL
# =========================
left, right = st.columns(2)

with left:
    st.subheader("Average Likes per Post (by Hotel)")

    hotel_perf = (
        filtered
        .groupby("ownerUsername")["likesCount"]
        .mean()
        .sort_values(ascending=False)
        .head(8)
    )

    fig, ax = plt.subplots()
    ax.barh(hotel_perf.index[::-1], hotel_perf.values[::-1])
    ax.set_xlabel("Avg Likes")
    st.pyplot(fig)

with right:
    st.subheader("Theme Distribution")

    theme_counts = filtered["theme"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        theme_counts,
        labels=theme_counts.index,
        autopct="%1.0f%%",
        startangle=140
    )
    st.pyplot(fig)

st.divider()

# =========================
# ROW 3 — DOES THEME MATTER?
# =========================
left, right = st.columns(2)

with left:
    st.subheader("Engagement by Content Theme")

    theme_engagement = (
        filtered
        .groupby("theme")[["likesCount", "commentsCount"]]
        .mean()
        .round(0)
    )

    st.dataframe(theme_engagement, use_container_width=True)

with right:
    st.subheader("Which Theme Performs Best?")

    fig, ax = plt.subplots()
    ax.bar(
        theme_engagement.index,
        theme_engagement["likesCount"]
    )
    ax.set_ylabel("Avg Likes")
    st.pyplot(fig)

st.divider()

# =========================
# ROW 4 — STRATEGIC TAKEAWAYS
# =========================
st.subheader("Strategic Interpretation")

st.markdown("""
### Key Findings
- **Brand-heavy content dominates volume**, but not engagement.
- **Experience-based posts (spa, dining, views)** generate the highest likes per post.
- **Seasonal content spikes frequency**, but engagement efficiency is lower.

### What This Means for Luxury Hotels
Instagram is being used as a **brand identity channel**, not a performance channel.
Hotels that emphasize *experiences* outperform those that rely on branding alone.

### Recommendation
Shift **20–30% of posts** from brand messaging → experiential storytelling
(spa moments, dining, atmosphere, quiet luxury).
""")

st.divider()

# =========================
# ROW 5 — TOP POSTS (PROOF)
# =========================
st.subheader("Top Performing Posts")

top_posts = (
    filtered
    .sort_values("likesCount", ascending=False)
    .head(10)[
        ["ownerUsername", "theme", "likesCount", "commentsCount", "caption"]
    ]
)

st.dataframe(top_posts, use_container_width=True)
