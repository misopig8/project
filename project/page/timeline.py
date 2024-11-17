import streamlit as st
import pandas as pd

bus_chart = pd.read_csv('project/page/대구광역시_시내버스 정류소별_노선별_평균배차간격_20231117.csv', encoding='utf-8')

st.title('시내버스 정류장 타임라인')

station_name = st.text_input('정류장 이름을 입력하세요:')

if station_name:
    filtered_df = bus_chart[bus_chart['정류소'].str.contains(station_name, na=False)]

    if not filtered_df.empty:
        station_list = filtered_df['정류소'].unique()
        selected_station = st.selectbox('검색된 정류장 목록에서 선택하세요:', station_list)
        selected_data = filtered_df[filtered_df['정류소'] == selected_station]

        st.write(f"### {selected_station}에 대한 정보:")

        
        cols = st.columns(1,1,1,1,2)

        for index, row in selected_data.iterrows():
            with cols[0]:
                st.write(f"**노선**: {row['노선']}")
               
            with cols[1]:
                st.write(f"**첫차**: {row['첫차']}")
                
            with cols[2]:
                st.write(f"**막차**: {row['막차']}")
                
            with cols[3]:
                st.write(f"**배차시간**: {row['평균배차시간(분)']}분")
                
            with cols[4]:
                st.write(f"**시간표 유형**: {row['시간표유형']}")
                
           
    else:
        st.write(f"'{station_name}'에 해당하는 정류장이 없습니다.")
