import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm


st.title("일일 버스통행량 정보")

daily_move = pd.read_csv('project/page/대구광역시_시내버스 일별 이용객수_20170131..csv', encoding="utf-8")
bus_stops_data = pd.read_csv('project/page/대구광역시_시내버스 정류소 위치정보_20240924.csv', encoding="utf-8")

plt.rc("font", family = "Malgun Gothic")
sns.set(font="Malgun Gothic", rc={"axes.unicode_minus":False}, style='white')

m = folium.Map(location=[35.8714354, 128.601445], tiles='cartodbpositron', zoom_start=12)
for idx, row in bus_stops_data.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['정류소명'],
        icon=folium.Icon(color='red', icon = 'info-sign')
    ).add_to(m)

st.subheader('대구시 내 버스 정류장 분포')
folium_static(m)

