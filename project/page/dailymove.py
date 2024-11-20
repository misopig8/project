import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm


st.title("버스통행량 정보")

monthly_move = pd.read_csv('project/page/대구광역시_시내버스_월별이용자수.csv', encoding="utf-8")


@st.cache
def load_data():
    # CSV 파일을 로드 (인코딩 설정 변경)
    monthly_move = pd.read_csv('project/page/대구광역시_시내버스_월별이용자수.csv', encoding='utf-8-sig')
    
    # 따옴표와 쉼표를 제거하고 승차와 하차를 정수로 변환
    monthly_move['승차'] = monthly_move['승차'].str.replace('"', '').str.replace(',', '').astype(int)
    monthly_move['하차'] = monthly_move['하차'].str.replace('"', '').str.replace(',', '').astype(int)
    
    # 영어 월 약어를 숫자로 변환
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    
    # '년월' 컬럼에서 월을 숫자로 변환
    monthly_move['년월'] = monthly_move['년월'].apply(lambda x: '20' + x.split('-')[0] + '-' + month_map[x.split('-')[1]])

    # '년월'을 날짜 형식으로 변환
    monthly_move['년월'] = pd.to_datetime(monthly_move['년월'], format='%Y-%m')  # '년월'을 datetime 형식으로 변환

    return monthly_move


# 검색창 추가
search_query = st.text_input("검색할 정류소명을 입력하세요:", "")

# 검색 및 필터링
if search_query:
    # 검색어를 포함한 정류소 필터링
    search_results = monthly_move[monthly_move['정류소명'].str.contains(search_query, case=False, na=False)]
    
    if not search_results.empty:
        st.write(f"'{search_query}'에 대한 검색 결과:")
        
        # 검색 결과에서 선택된 정류소 하나를 선택할 수 있게 설정
        selected_stop = st.selectbox("정류소를 선택하세요:", search_results['정류소명'].unique())
        
        # 선택한 정류소의 월별 데이터 필터링
        selected_data = search_results[search_results['정류소명'] == selected_stop]
        
        # 월별 데이터 추출 및 전처리
        selected_data['년월'] = pd.to_datetime(selected_data['년월'], format='%y-%b')
        selected_data = selected_data.sort_values('년월')
        
        # 그래프 생성
        plt.figure(figsize=(10, 5))
        
        plt.ticklabel_format(axis='y', style='plain')
        # 승차 데이터 추가
        plt.plot(selected_data['년월'], selected_data['승차'], marker='o', label='seungcha')
        
        # 하차 데이터 추가
        plt.plot(selected_data['년월'], selected_data['하차'], marker='x', label='hacha')
        
        # 그래프 레이아웃 설정
        plt.title(f"{selected_stop} monthly seungcha and hacha people.")
        plt.xlabel("month")
        plt.ylabel("people")
        plt.legend()
        plt.ylim(0, selected_data[['승차', '하차']].max().max() * 1.1)  # 여유를 두기 위해 10% 증가시킴

        # 그래프를 Streamlit에 표시
        st.pyplot(plt)
    else:
        st.write(f"'{search_query}'에 해당하는 정류소가 없습니다.")
else:
    st.write("정류소명을 입력하여 검색하세요.")
