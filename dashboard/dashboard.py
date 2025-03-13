import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_byseasonday_df(df):
    byseasonday_df = df.groupby(by='season')['cnt'].sum().reset_index()
    byseasonday_df.rename(columns={
        'cnt': 'total_sewa'
    }, inplace=True)
    
    return byseasonday_df


def create_byweekday_df(df):
    byweekday_df = df.groupby(by='weekday')['cnt'].mean().reset_index()
    byweekday_df.rename(columns={
        'cnt': 'rata_sewa'
    }, inplace=True)

    return byweekday_df

def create_byhour_df(df):
    byhour_df = jam_df.groupby(by='hr')['cnt'].mean().reset_index()
    byhour_df.rename(columns={
        'cnt': 'rata_sewa'
    }, inplace=True)

    sorting = byhour_df.sort_values(by='rata_sewa', ascending=False)

    highest = sorting.head(10)

    return highest

def create_byweathersit(df):
    byweathersit_df = df.groupby(by='weathersit')['cnt'].mean().reset_index()
    byweathersit_df.rename(columns={
        'cnt': 'mean_sewa'
    }, inplace=True)

    return byweathersit_df

hari_df = pd.read_csv('dashboard/hari_file.xls')
jam_df = pd.read_csv('dashboard/jam_file.xls')


jam_df['dteday'] = pd.to_datetime(jam_df['dteday'])

min_date = jam_df["dteday"].min()
max_date = jam_df["dteday"].max()

datetime_columns = ['dteday']
jam_df.sort_values(by="dteday", inplace=True)
jam_df.reset_index(inplace=True)
 
for column in datetime_columns:
    jam_df[column] = pd.to_datetime(jam_df[column])

 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    st.write(
        """
        # Annyeong-haseo everyone
        This is not about Collection, but this is Bike Sharing
        """
    )

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = jam_df[(jam_df["dteday"] >= start_date) &  
                 (jam_df["dteday"] <= end_date)] 

byweekday_df = create_byweekday_df(main_df)
byhour_df = create_byhour_df(main_df)
highest = byhour_df.sort_values(by='hr')
byweathersit_df = create_byweathersit(main_df)
byseasonday_df = create_byseasonday_df(main_df)

season_labels = {1:'Semi', 2:'Panas', 3:'Gugur', 4:'Dingin'}
byseasonday_df['season'] = byseasonday_df['season'].replace(season_labels)

weekday_labels = {0:'Senin', 1:'Selasa', 2:'Rabu', 3:'Kamis', 4:'Jumat', 5:'Sabtu', 6:'Minggu'}
byweekday_df['weekday'] = byweekday_df['weekday'].replace(weekday_labels)

st.header('Dicoding Bike Sharing Dashboard :sparkles:')

st.subheader("Tren Penyewaan")
col1, col2 = st.columns([1,2])

with col1:
    st.write("")
    st.write("")
    st.write("")
    total_rentals = main_df.cnt.sum()
    st.metric("Total Penyewaan", value=total_rentals)
    st.write("")
    avg_rentals = main_df.cnt.mean()
    st.metric("Average Penyewaan", value=f"{avg_rentals:.2f}")

with col2:
    
    fig, ax = plt.subplots(figsize=(20, 15))
    colors_ = ["#D3D3D3", "#D3D3D3", "#4F959D", "#D3D3D3"]

    plt.bar(
        byseasonday_df['season'], 
        byseasonday_df['total_sewa'], 
        color=colors_
    )
    ax.set_title('Berdasarkan Musim', fontsize=50)
    ax.set_xlabel('Musim', fontsize=40)
    ax.set_ylabel('Total Sewa', fontsize=40)

    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)

    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots(figsize=(20, 15))

    ax.plot(
        byweekday_df['weekday'],
        byweekday_df['rata_sewa'],
        marker='o',
        markersize=20,
        linewidth=4,
        color='#4F959D'
    )

    ax.set_title("Berdasarkan Hari", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel(None)

    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)

    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots(figsize=(20, 15))

    sorted_hour = byhour_df.sort_values(by='hr')

    ax.plot(
        highest['hr'],
        highest['rata_sewa'],
        marker='o',
        markersize=20,
        linewidth=4,
        color='#4F959D'
    )

    ax.set_title("Berdasarkan Jam", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel(None)

    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)

    st.pyplot(fig)

st.subheader("Faktor Cuaca")
weather_labels = {1:'Cerah', 2:'Berkabut', 3:'Salju ringan', 4:' Cuaca ekstream'}
byweathersit_df['weathersit'] = byweathersit_df['weathersit'].replace(weather_labels)
fig, ax = plt.subplots(figsize=(20, 15))
colors_2 = ["#4F959D", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

plt.bar(
    byweathersit_df['weathersit'], 
    byweathersit_df['mean_sewa'], 
    color=colors_2
)
ax.set_title('Rata-rata Penyewaan', fontsize=50)
ax.set_xlabel('Musim', fontsize=40)
ax.set_ylabel('Total Sewa', fontsize=40)

ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=35)

st.pyplot(fig)