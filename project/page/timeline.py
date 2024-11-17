import streamlit as st
import pandas as pd

# CSV 파일을 pandas로 읽기
bus_chart = pd.read_csv('project/page/대구광역시_시내버스 정류소별_노선별_평균배차간격_20231117.csv', encoding='utf-8')

# Streamlit 앱 타이틀
st.title('대구광역시 시내버스 정류장 정보 검색')

# 사용자 입력을 통해 정류장 이름 검색
station_name = st.text_input('정류장 이름을 입력하세요:')

if station_name:
    # 입력한 정류장 이름에 해당하는 데이터를 필터링
    filtered_df = bus_chart[bus_chart['정류소'].str.contains(station_name, na=False)]

    # 정류장 이름이 있는 경우
    if not filtered_df.empty:
        # 정류장 목록을 선택할 수 있는 selectbox 제공
        station_list = filtered_df['정류소'].unique()
        selected_station = st.selectbox('검색된 정류장 목록에서 선택하세요:', station_list)

        # 선택된 정류장의 데이터만 필터링
        selected_data = filtered_df[filtered_df['정류소'] == selected_station]

        st.write(f"### {selected_station}에 대한 정보:")
        for index, row in selected_data.iterrows():
            st.write(f"**노선**: {row['노선']}")
            st.write(f"**평균 배차 시간**: {row['평균배차시간(분)']}분")
            st.write(f"**첫차 시간**: {row['첫차']}")
            st.write(f"**막차 시간**: {row['막차']}")
            st.write("---")
    else:
        st.write(f"'{station_name}'에 해당하는 정류장이 없습니다.")
