import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


day_df = pd.read_csv('day.csv')
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

day_df['season'] = day_df.season.astype('category')
day_df['yr'] = day_df.yr.astype('category')
day_df['mnth'] = day_df.mnth.astype('category')
day_df['holiday'] = day_df.holiday.astype('category')
day_df['weekday'] = day_df.weekday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')
day_df.info()

day_df['mnth'] = day_df['mnth'].map({
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'
})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty and Cloudy',
    3: 'Light Snow/Light Rain',
    4: 'Heavy Rain, Snow, and Mist'
})
day_df['yr'] = day_df['yr'].map({
    0: '2011', 1: '2012'
})
day_df.head()


min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/YosafatGA/Data-visualization-project/blob/main/Assets/bike-sharing-service-high-resolution-logocrop.png?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# Membuat berbagai dataframe yang diperlukan
# Dataframe user casual dan registered tiap tahun
cr_user_yr_df = day_df.groupby(by=["yr"]).agg({
    "casual": "sum",
    "registered": "sum",
}).reset_index()
cr_user_yr_df.rename(columns={
    "yr": "year",
}, inplace=True)
cr_user_yr_melt_df = cr_user_yr_df.melt(id_vars="year")

# Dataframe total user tiap tahun
count_yr_df = day_df.groupby(by=["yr"]).agg({
    "cnt": "sum"
}).reset_index()

# Dataframe user tiap bulan
monthly_df = day_df.groupby(by=["yr", "mnth"]).agg({
    "cnt": "sum"
}).reset_index()

# Dataframe user tiap musim
season_df = day_df.groupby(by=["yr", "season"]).agg({
    "cnt": "sum"
}).reset_index()
season_df.rename(columns={
    "yr": "year",
    "cnt": "total_user"
}, inplace=True)

# Dataframe user tiap cuaca
weather_df = day_df.groupby(by=["yr", "weathersit"]).agg({
    "cnt": "sum"
}).reset_index()
weather_df.rename(columns={
    "yr": "year",
    "cnt": "total_user"
}, inplace=True)


st.header('Bike Sharing Dashboard :bike:')


st.subheader('Casual and Registered User Each Year')

colors = ["#EA906C", "#B31312"]

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    y="value",
    x="variable",
    hue="year",
    data=cr_user_yr_melt_df,
    palette=colors,
    ax=ax
)
ax.set_ylabel("Total user")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)


st.subheader("Total User Each Year")

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    y="cnt",
    x="yr",
    data=count_yr_df.sort_values(by="cnt", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_ylabel("Total user")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)


st.subheader("Total User Each Month")

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    data=monthly_df,
    x="mnth",
    y="cnt",
    hue="yr",
    palette="viridis",
    marker="o",
    ax=ax
)
ax.set_xlabel(None)
ax.tick_params(axis='x', rotation=45)
ax.set_ylabel("Total user")
ax.legend(title="Year", loc="upper right")

st.pyplot(fig)


st.subheader(("Total User Each Season"))

fig, ax = plt.subplots(figsize=(16, 8))
colors = ["#EA906C", "#B31312"]
sns.barplot(
    y="total_user",
    x="season",
    hue="year",
    data=season_df,
    palette=colors,
    ax=ax
)
ax.set_ylabel("Total user")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)


st.subheader(("Total User Each Weather"))

fig, ax = plt.subplots(figsize=(16, 8))
colors = ["#EA906C", "#B31312"]
sns.barplot(
    y="total_user",
    x="weathersit",
    hue="year",
    data=weather_df,
    palette=colors,
    ax=ax
)
ax.set_ylabel("Total user")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)
 
st.caption('Copyright (c) Bike Sharing Service 2023')
