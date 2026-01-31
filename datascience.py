import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="NYC Airbnb Dashboard",
    layout="wide"
)


df = pd.read_csv("AB_NYC_2019.csv")

df = df.drop(columns=["name", "host_name"], errors="ignore")
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)
df = df[df["price"] <= 1000]
df = df[df["minimum_nights"] <= 365]
df = df.reset_index(drop=True)

# I created a few extra columns to help compare
# cheaper vs more expensive listings more easily

df["price_per_review"] = df["price"] / (df["number_of_reviews"] + 1)
# +1 is used so listings with 0 reviews don't cause division errors

df["price_label"] = "Cheap"
df.loc[df["price"] > 150, "price_label"] = "Expensive"


st.sidebar.header("Filters")

st.sidebar.markdown(
    """
Use the slider below to focus on Airbnb listings within a specific price range.
Changing the price range will update all charts and metrics in the dashboard.
    """
)

price_options = sorted(df["price"].unique())

min_price, max_price = st.sidebar.select_slider(
    "Price Range (USD)",
    options=price_options,
    value=(price_options[0], price_options[-1]),
    format_func=lambda x: f"${x}"
)

price_mask = (df["price"] >= min_price) & (df["price"] <= max_price)
df_filtered = df[price_mask]


st.title("NYC Airbnb Market Dashboard")
st.caption("This dashboard explores how Airbnb prices and reviews vary across NYC boroughs and listing types.")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Listings", f"{len(df_filtered):,}", border=True)

avg_price = df_filtered["price"].mean()
m2.metric("Average Price ($)", f"{avg_price:.1f}", border=True)

m3.metric(
    "Average Reviews per Listing",
    f"{df_filtered['number_of_reviews'].mean():.1f}",
    border=True
)

m4.metric(
    "Cheap Listings (%)",
    f"{(df_filtered['price_label'] == 'Cheap').mean() * 100:.1f}%",
    border=True
)

with st.expander("View Raw Data"):
    st.dataframe(df_filtered)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Average Price by Borough")
    price_by_borough = df_filtered.groupby("neighbourhood_group")["price"].mean()
    avg_price = price_by_borough
    plt.figure()
    avg_price.plot(kind="bar", color="skyblue")
    plt.xlabel("Borough")
    plt.ylabel("Average Price (USD)")
    plt.xticks(rotation=45)
    st.caption(
    "This chart shows how the average Airbnb price differs across NYC boroughs. Manhattan has the highest average prices, while the Bronx has the lowest, highlighting how location strongly affects listing cost."
    )
    st.pyplot(plt)
    plt.clf()

with c2:
    st.subheader("Average Reviews by Price Category")
    avg_reviews = df_filtered.groupby("price_label")["number_of_reviews"].mean()
    plt.figure()
    avg_reviews.plot(kind="bar", color=["lightgreen", "salmon"])
    plt.xlabel("Price Category")
    plt.ylabel("Average Number of Reviews")
    st.caption(
    "This chart compares the average number of reviews between cheap and expensive listings. Cheaper listings tend to receive more reviews, suggesting they may attract more frequent bookings."
    )
    st.pyplot(plt)
    plt.clf()

c3, c4 = st.columns(2)

with c3:
    st.subheader("Price vs Number of Reviews")
    fig = plt.figure()
    plt.scatter(df_filtered["price"], df_filtered["number_of_reviews"], alpha=0.3)
    plt.xlabel("Price (USD)")
    plt.ylabel("Total Reviews")
    st.caption(
    "This scatter plot shows the relationship between price and total reviews. Lower-priced listings generally receive more reviews, while higher-priced listings tend to have fewer reviews overall."
    )
    st.pyplot(fig)
    plt.clf()

with c4:
    st.subheader("Room Type Distribution by Borough")
    stacked_chart = df_filtered.pivot_table(
        index="neighbourhood_group",
        columns="room_type",
        values="price",
        aggfunc="count",
        fill_value=0
    )

    plt.figure()
    plt.bar(stacked_chart.index, stacked_chart["Entire home/apt"], label="Entire home/apt")
    plt.bar(
        stacked_chart.index,
        stacked_chart["Private room"],
        bottom=stacked_chart["Entire home/apt"],
        label="Private room"
    )
    plt.bar(
        stacked_chart.index,
        stacked_chart["Shared room"],
        bottom=stacked_chart["Entire home/apt"] + stacked_chart["Private room"],
        label="Shared room"
    )
    plt.xlabel("Borough")
    plt.ylabel("Number of Listings")
    plt.xticks(rotation=45)
    st.caption(
    "This chart shows how different room types are distributed across NYC boroughs. Entire homes and private rooms dominate the market, especially in Manhattan and Brooklyn, while shared rooms are relatively rare."
    )
    plt.legend()
    st.pyplot(plt)
    plt.clf()
