import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def load_monthly_move_data():
    return pd.read_csv('project/page/대구광역시_시내버스_월별이용자수.csv', encoding="utf-8")


@st.cache_data
def load_bus_stops_data():
    return pd.read_csv('project/page/대구광역시_시내버스 정류소 위치정보_20240924.csv', encoding="utf-8")


@st.cache_data
def create_map(data):
    m = folium.Map(location=[35.8714354, 128.601445], tiles='cartodbpositron', zoom_start=20)
    for idx, row in data.iterrows():
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=row['정류소명'],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    return m


@st.cache_data
def process_selected_data(selected_data):
    selected_data['년월'] = pd.to_datetime(selected_data['년월'], format='%y-%b')
    selected_data = selected_data.sort_values('년월')
    return selected_data


st.title("버스통행량 정보")

# 데이터 로딩 (캐시 적용됨)
monthly_move = load_monthly_move_data()
bus_stops_data = load_bus_stops_data()

# 지도 생성 및 표시
st.subheader('대구시 내 버스 정류장 분포')
m = create_map(bus_stops_data)
folium_static(m)

# 검색창 추가
search_query = st.text_input("찾는 정류장의 이름을 입력하세요:", "")

if search_query:
    # 검색 기능 구현
    search_results = monthly_move[monthly_move['정류소명'].str.contains(search_query, case=False, na=False)]
    
    if not search_results.empty:
        st.write(f"'{search_query}'에 대한 검색 결과:")
        st.write(search_results)
    else:
        st.write(f"'{search_query}'에 대한 검색 결과가 없습니다.")
else:
    st.write("모든 버스 정류장 데이터:")
    st.write(monthly_move)

# 검색창 추가
search_query = st.text_input("검색할 정류소명을 입력하세요:", "")

# 검색 및 필터링
if search_query:
    search_results = bus_stops_data[bus_stops_data['정류소명'].str.contains(search_query, case=False, na=False)]
    
    if not search_results.empty:
        st.write(f"'{search_query}'에 대한 검색 결과:")
        
        selected_stop = st.selectbox("정류소를 선택하세요:", search_results['정류소명'].unique())
        
        selected_data = search_results[search_results['정류소명'] == selected_stop]
        processed_data = process_selected_data(selected_data)

        plt.figure(figsize=(10, 5))
        plt.plot(processed_data['년월'], processed_data['승차'], marker='o', label='승차')
        plt.plot(processed_data['년월'], processed_data['하차'], marker='x', label='하차')

        plt.title(f"{selected_stop} 정류장의 월별 승차 및 하차 인원")
        plt.xlabel("월")
        plt.ylabel("이용자 수")
        plt.legend()

        st.pyplot(plt)
    else:
        st.write(f"'{search_query}'에 해당하는 정류소가 없습니다.")
else:
    st.write("정류소명을 입력하여 검색하세요.")
