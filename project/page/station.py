import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

st.title("대구 내 버스 정거장 정보")

plt.rc("font", family = "Malgun Gothic")
sns.set(font="Malgun Gothic", rc={"axes.unicode_minus":False}, style='white')
bus_stops_data = pd.read_csv('page/대구광역시_시내버스 정류소 위치정보_20240924.csv', encoding="utf-8")
top_bus_stops_data = pd.read_csv("page/한국교통안전공단_대구광역시 최다 이용 정류장_20231231.csv", encoding="utf-8")

most_used_bus_stops = {
    "약령시건너(동성로입구)(7001003800)": {"위도": 35.867842, "경도": 128.593687},	
    "약령시앞(7001004100)": {"위도": 35.868969, "경도": 128.593601},
    "동대구역건너(7011006800)": {"위도": 35.878697, "경도": 128.626813},
    "아양교역(1번출구)(7011011000)": {"위도": 35.887137, "경도": 128.639467},
    "2.28기념중앙공원앞(7001006800)": {"위도": 35.870309, "경도": 128.598316},
    "경상감영공원앞(7001004600)": {"위도": 35.873766, "경도": 128.594496},
    "경상감영공원건너(7001004300)": {"위도": 35.872771, "경도": 128.594449},
    "동대구역(7011006700)": {"위도": 35.879173, "경도": 128.626983},
    "아양교역(2번출구)(7011010900)": {"위도": 35.887059, "경도": 128.639898},
    "동구청건너(7011010600)": {"위도": 35.885766, "경도": 128.634791}
}


m = folium.Map(location=[35.8714354, 128.601445], tiles='cartodbpositron', zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# 버스 정류장 마커 추가
for idx, row in bus_stops_data.iterrows():
    if row['정류소명'] in most_used_bus_stops:
        most_used_info = most_used_bus_stops[row['정류소명']]
        folium.Marker(
            location=[most_used_info['위도'], most_used_info['경도']],
            popup=row['정류소명'],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    else:
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=row['정류소명']
        ).add_to(marker_cluster)

# 지도 출력
st.subheader('대구시 내 버스 정류장 분포')
folium_static(m)

#---------------------------------------------------

# 정류소명이 문자열인지 확인 후 변환!! GPT는 신이야
top_bus_stops_data['정류소명'] = top_bus_stops_data['정류소명'].astype(str)

# #//////////////////

# 최다 이용 정류장 분석
st.subheader('최다 이용 정류장 분석')

# 최다 이용 정류장 선택
selected_bus_stop = st.selectbox('최다 이용 정류장을 선택하세요.', top_bus_stops_data['정류소명'])

# 전체 최다 이용 정류장 데이터프레임 출력
styled_most_used_bus_stops_data = top_bus_stops_data.copy()
styled_most_used_bus_stops_data['선택'] = styled_most_used_bus_stops_data['정류소명'].apply(lambda x: "📌" if x == selected_bus_stop else '')
st.write(styled_most_used_bus_stops_data)

# 선택한 정류장 위치 확인
if selected_bus_stop in most_used_bus_stops:
    most_used_info = most_used_bus_stops[selected_bus_stop]
    selected_stop_location = pd.DataFrame({'위도': [most_used_info['위도']], '경도': [most_used_info['경도']]})
else:
    selected_stop_location = bus_stops_data.loc[bus_stops_data['정류소명'] == selected_bus_stop, ['위도', '경도']]

# 선택한 정류장이 데이터에 있는지 확인
if not selected_stop_location.empty:
    selected_stop_location = selected_stop_location.iloc[0]

  # 선택한 정류장을 강조하여 지도에 출력
    m = folium.Map(location=[selected_stop_location['위도'], selected_stop_location['경도']], zoom_start=15)

    # 선택한 정류장을 빨간 마커로 추가
    folium.Marker(
        location=[selected_stop_location['위도'], selected_stop_location['경도']],
        popup=selected_bus_stop,
        icon=folium.Icon(color='red', icon='star')
    ).add_to(m)

    # 나머지 최다 이용 정류장들을 초록 마커로 개별적으로 추가
    for idx, row in top_bus_stops_data.iterrows():
        if row['정류소명'] != selected_bus_stop and row['정류소명'] in most_used_bus_stops:
            most_used_info = most_used_bus_stops[row['정류소명']]
            folium.Marker(
                location=[most_used_info['위도'], most_used_info['경도']],
                popup=row['정류소명'],
                icon=folium.Icon(color='gray', icon='star')
            ).add_to(m)

    # 나머지 정류장들을 클러스터로 그룹화하여 추가
    other_stops = bus_stops_data[~bus_stops_data['정류소명'].isin(most_used_bus_stops.keys())]
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in other_stops.iterrows():
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=row['정류소명']
        ).add_to(marker_cluster)

    # 지도 출력
    st.subheader('선택한 최다 이용 정류장 위치')
    folium_static(m)
else:
    st.error(f"Selected bus stop '{selected_bus_stop}' not found in the dataset.")

    
# 선택된 행의 배경색 지정
highlight_color = 'lightcoral'

# 선택된 행에 배경색을 적용하는 함수
def highlight_row(row):
    if row['정류소명'] == selected_bus_stop:
        return [f'background-color: {highlight_color}' for _ in row]
    else:
        return ['' for _ in row]

# 선택된 행에 배경색을 적용한 데이터프레임 생성
styled_selected_bus_stop_data = top_bus_stops_data[top_bus_stops_data['정류소명'] == selected_bus_stop].style.apply(highlight_row, axis=1)

# 스타일이 적용된 표 출력
st.write(styled_selected_bus_stop_data)

# 지도 생성
m = folium.Map(location=[36.350411, 127.384548], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# 최다 이용 정류장을 빨간 마커로 표시
for idx, row in top_bus_stops_data.iterrows():
    if row['정류소명'] in most_used_bus_stops:
        most_used_info = most_used_bus_stops[row['정류소명']]
        folium.Marker(
            location=[most_used_info['위도'], most_used_info['경도']],
            popup=row['정류소명'],
            icon=folium.Icon(color='red', icon='star')
        ).add_to(m)

