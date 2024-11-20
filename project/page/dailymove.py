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

        # 그래프를 Streamlit에 표시
        st.pyplot(plt)

        
#코드 작동 테스트라인. 왜 안되지 십발
        st.dataframe(selected_data)
 
#  #코드 작동 테스트라인2 이거 안되면 진짜
        selected_data["월"] = selected_data["년월"].dt.month  # 월 추출
        selected_data["년"] = selected_data["년월"].dt.year  # 년도 추출 (필요 시)

# # 월별 평균 계산 (가장 단순한 방법으로 월별 합계나 평균을 구할 수 있습니다)
        monthly_data = selected_data.groupby("월")[["승차", "하차"]].mean()

# # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(monthly_data.index, monthly_data["승차"], label="승차", marker="o")
        ax.plot(monthly_data.index, monthly_data["하차"], label="하차", marker="s")

# # 그래프 설정
        ax.set_title("2020년 월별 승차와 하차 추이")
        ax.set_xlabel("월")
        ax.set_ylabel("값")
        ax.set_xticks(monthly_data.index)  # X축에 월 표시
        ax.set_xticklabels(["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"])
        ax.legend()

        # Streamlit에서 그래프 표시
        st.pyplot(fig)
    else:
        st.write(f"'{search_query}'에 해당하는 정류소가 없습니다.")
else:
    st.write("정류소명을 입력하여 검색하세요.")