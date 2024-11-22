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

# 테이블 데이터 조회
def fetch_data():
    sql = "SELECT * FROM projectuser"
    cursor.execute(sql)
    rows = cursor.fetchall()  # 모든 데이터 가져오기
    columns = [desc[0] for desc in cursor.description]  # 컬럼 이름 가져오기
    return pd.DataFrame(rows, columns=columns)  # DataFrame으로 반환

# Streamlit UI
st.title("회원 데이터 조회")

# 데이터 불러오기 버튼
if st.button("데이터 불러오기"):
    try:
        df = fetch_data()
        if not df.empty:
            st.success("데이터를 성공적으로 불러왔습니다!")
            st.dataframe(df)  # 데이터를 Streamlit의 DataFrame 형태로 보여주기
        else:
            st.warning("데이터가 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")
    finally:
        conn.close()  # 연결 닫기



# 초기 위치 설정 (위도, 경도)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 서울 시청 위치

# 지도에 마커 추가
folium.Marker([37.5665, 126.9780], popup="서울 시청", tooltip="서울").add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=700, height=500)


