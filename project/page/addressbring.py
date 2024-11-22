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
conn = sqlite3.connect('db.db')
cursor = conn.cursor()
import streamlit as st
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# 특정 사용자의 station_number 조회 함수
def get_station_number(username):
    sql = "SELECT station_number FROM projectuser WHERE username = ?"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()  # 하나의 결과만 가져옴
    return result[0] if result else None  # 결과가 있으면 첫 번째 값 반환, 없으면 None

# Streamlit UI
st.title("정류장 번호 조회")

# 사용자 이름 입력
username = st.text_input("사용자 이름 입력:")

# 조회 버튼
if st.button("정류장 번호 조회"):
    station_number = get_station_number(username)
    if station_number:
        st.success(f"{username}님의 정류장 번호는: {station_number}")
        # 변수에 저장
        selected_station_number = station_number
        st.write(f"저장된 변수: {selected_station_number}")
    else:
        st.warning("해당 사용자를 찾을 수 없습니다.")

# 데이터베이스 연결 닫기
conn.close()


# 초기 위치 설정 (위도, 경도)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 서울 시청 위치

# 지도에 마커 추가
folium.Marker([37.5665, 126.9780], popup="서울 시청", tooltip="서울").add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=700, height=500)


