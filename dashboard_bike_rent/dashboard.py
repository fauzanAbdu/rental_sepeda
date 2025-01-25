import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    # Mengelompokkan data berdasarkan tanggal untuk agregasi harian
    daily_orders_df = df.groupby('dteday').agg({
        "cnt_x": "sum"  # Menjumlahkan total rental sepeda harian
    }).reset_index()
    # Menambahkan nama kolom yang lebih deskriptif
    daily_orders_df.rename(columns={
        "dteday": "order_date",  # Mengubah nama kolom tanggal
        "cnt_x": "order_count"    # Mengubah nama kolom jumlah rental
    }, inplace=True)
    
    return daily_orders_df

def create_sum_rent_bike_df(df):
    sum_rent_bike_df = df.groupby("season_x").cnt_x.sum().sort_values(ascending=False).reset_index()
    sum_rent_bike_df.rename(columns={
        "dteday": "order_date",  # Mengubah nama kolom tanggal
        "cnt_x": "order_count"    # Mengubah nama kolom jumlah rental
    }, inplace=True)
    return sum_rent_bike_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season_x").cnt_x.sum().reset_index()
    byseason_df['season_x'] = pd.Categorical(byseason_df['season_x'])
    byseason_df.rename(columns={
        "dteday": "order_date",  # Mengubah nama kolom tanggal
        "cnt_x": "order_count"    # Mengubah nama kolom jumlah rental
    }, inplace=True)
    return byseason_df

def create_bymonth_df(df):
    bymonth_df = df.groupby(by="mnth_x").cnt_x.sum().reset_index()
    bymonth_df['mnth_x'] = pd.Categorical(bymonth_df['mnth_x'])
    bymonth_df.rename(columns={
        "dteday": "order_date",  # Mengubah nama kolom tanggal
        "cnt_x": "order_count"    # Mengubah nama kolom jumlah rental
    }, inplace=True)    
    return bymonth_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday_x").cnt_x.sum().reset_index()
    byweekday_df['weekday_x'] = pd.Categorical(byweekday_df['weekday_x'])
    byweekday_df.rename(columns={
        "dteday": "order_date",  # Mengubah nama kolom tanggal
        "cnt_x": "order_count"    # Mengubah nama kolom jumlah rental
    }, inplace=True)     
    return byweekday_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit_x").cnt_x.sum().reset_index()
    byweather_df['weathersit_x'] = pd.Categorical(byweather_df['weathersit_x'])
    byweather_df.rename(columns={
        "dteday": "order_date",  # Mengubah nama kolom tanggal
        "cnt_x": "order_count"    # Mengubah nama kolom jumlah rental
    }, inplace=True)     
    return byweather_df

#membuat fungsi highlight
def highlight_max(df, column):
    is_max = df[column] == df[column].max()
    return ['#FFA726' if v else '#90CAF9' for v in is_max]

hour_day_df = pd.read_csv("hour_day.csv")

datetime_columns = ["dteday"]
hour_day_df.sort_values(by="dteday", inplace=True)
hour_day_df.reset_index(inplace=True)

for column in datetime_columns:
    hour_day_df[column] = pd.to_datetime(hour_day_df[column])

min_date = hour_day_df["dteday"].min()
max_date = hour_day_df["dteday"].max()
filtered_df = hour_day_df[(hour_day_df['dteday'] >= min_date) & (hour_day_df['dteday'] <= max_date)]

with st.sidebar:
    st.image("https://raw.githubusercontent.com/fauzanAbdu/proyek-analis-data/5294f4a99035c27fca54c24818c2ae097aaf455e/Free_Bike_rental_PosterMyWall.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = hour_day_df[(hour_day_df['dteday'] >= str(start_date)) & 
                    (hour_day_df['dteday'] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_rent_bike_df = create_sum_rent_bike_df(main_df)
bymonth_df = create_bymonth_df(main_df)
byweekday_df = create_byweekday_df(main_df)
byweather_df = create_byweather_df(main_df)
byseason_df = create_byseason_df(main_df)

st.header('Dicoding Bike Rent Dashboard :sparkles:')

st.subheader('Daily Rent')

col1, _ = st.columns(2)

with col1:
    total_rent = daily_orders_df.order_count.sum()
    st.metric("total_rent", value=total_rent)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_date"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x',rotation=45, labelsize=15)
ax.grid(True)
st.pyplot(fig)

st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    season_mapping = {
        1: "Clear/Partly Cloudy",
        2: "Mist/Cloudy",
        3: "Light Rain/Snow",
        4: "Heavy Rain/Snow"}
    byweather_df["weathersit_x"] = byweather_df["weathersit_x"].map(season_mapping)
    colors = highlight_max(byweather_df, 'order_count')
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="order_count",
        x="weathersit_x",
        data=byweather_df.sort_values(by="order_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Customer Rent Bike by Weather", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    season_mapping = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"}
    byseason_df["season_x"] = byseason_df["season_x"].map(season_mapping)
    colors = highlight_max(byseason_df, 'order_count')
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
    y="order_count",
    x="season_x",
    data=byseason_df.sort_values(by="order_count", ascending=False),
    palette=colors
    )
    ax.set_title("Customer Rent Bike by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20,10))
weekday_mapping = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Satuday"
}
byweekday_df["weekday_x"] = byweekday_df["weekday_x"].map(weekday_mapping)
colors = highlight_max(byweekday_df, 'order_count')
sns.barplot(
    x="order_count",
    y="weekday_x",
    data=byweekday_df.sort_values(by="order_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Customer Rent Bike by Weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20,10))
colors = highlight_max(bymonth_df, 'order_count')
sns.barplot(
    x="order_count",
    y="mnth_x",
    data=bymonth_df.sort_values(by="order_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Customer Rent Bike by month", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)