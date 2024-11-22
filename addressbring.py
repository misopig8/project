import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import sqlite3
st.title("내 주소")
bus_stops_data = pd.read_csv('project/page/대구광역시_시내버스 정류소 위치정보_20240924.csv', encoding="utf-8")


# 데이터베이스 연결
# SQLite DB 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# Step 1: Username 기반으로 station_number 조회
st.title("정류장 조회 및 위/경도 검색")

username = st.text_input("사용자 아이디를 입력하세요:")

if st.button("정류장 번호 조회"):
    if username:
        # username을 기반으로 station_number 조회
        cursor.execute("SELECT station_number FROM projectuser WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result:
            station_number = result[0]  # station_number 값 저장
            st.success(f"사용자의 정류장 번호: {station_number}")

            # Step 2: station_number를 기준으로 CSV에서 위도와 경도 조회
            station_data = bus_stops_data[bus_stops_data['정류소아이디'] == int(station_number)]

            if not station_data.empty:
                latitude = station_data.iloc[0]['위도']
                longitude = station_data.iloc[0]['경도']

                st.write(f"정류장의 위도: {latitude}, 경도: {longitude}")
                m = folium.Map(location=[latitude, longitude], zoom_start=12)  # 서울 시청 위치

# 지도에 마커 추가
                folium.Marker([latitude, longitude], popup="나의 정류장 위치", tooltip="버스").add_to(m)

# Streamlit에 지도 표시     
                st_folium(m, width=700, height=500)
            else:
                st.error("CSV에서 해당 정류장 번호를 찾을 수 없습니다.")
        else:
            st.error("DB에 해당 사용자가 없습니다.")
    else:
        st.error("사용자 아이디를 입력해주세요.")

# DB 연결 종료
conn.close()

# 데이터베이스 연결 닫기
conn.close()


# 초기 위치 설정 (위도, 경도)



