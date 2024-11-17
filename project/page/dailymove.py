# import streamlit as st
# from streamlit_folium import folium_static
# import folium
# from folium.plugins import MarkerCluster
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import matplotlib.font_manager as fm


# st.title("버스통행량 정보")

# monthly_move = pd.read_csv('project/page/대구광역시_시내버스_월별이용자수.csv', encoding="utf-8")
# bus_stops_data = pd.read_csv('project/page/대구광역시_시내버스 정류소 위치정보_20240924.csv', encoding="utf-8")

# plt.rc("font", family = "Malgun Gothic")
# sns.set(font="Malgun Gothic", rc={"axes.unicode_minus":False}, style='white')

# m = folium.Map(location=[35.8714354, 128.601445], tiles='cartodbpositron', zoom_start=20)
# for idx, row in bus_stops_data.iterrows():
#     folium.Marker(
#         location=[row['위도'], row['경도']],
#         popup=row['정류소명'],
#         icon=folium.Icon(color='red', icon = 'info-sign')
#     ).add_to(m)

# st.subheader('대구시 내 버스 정류장 분포')
# folium_static(m)

# # 검색창 추가
# search_query = st.text_input("찾는 정류장의 이름을입력하세요", "")

# # 검색 기능 구현
# if search_query:
#     # 입력한 검색어가 포함된 행만 필터링
#     search_results = monthly_move[monthly_move['정류소명'].str.contains(search_query, case=False, na=False)]
    
#     # 결과가 있다면 출력
#     if not search_results.empty:
#         st.write(f"'{search_query}'에 대한 검색 결과:")
#         st.write(search_results)
#     else:
#         st.write(f"'{search_query}'에 대한 검색 결과가 없습니다.")
# else:
#     # 초기에는 전체 데이터 출력
#     st.write("모든 버스 정류장 데이터:")
#     st.write(monthly_move)

# #재출력문

# # CSV 파일 로드
# file_path = 'project/page/대구광역시_시내버스 정류소 위치정보_20240924.csv'
# bus_stops_data = pd.read_csv(file_path, encoding='utf-8')

# # 검색창 추가
# search_query = st.text_input("검색할 정류소명을 입력하세요:", "")

# # 검색 및 필터링
# if search_query:
#     # 검색어를 포함한 정류소 필터링
#     search_results = bus_stops_data[bus_stops_data['정류소명'].str.contains(search_query, case=False, na=False)]
    
#     if not search_results.empty:
#         st.write(f"'{search_query}'에 대한 검색 결과:")
        
#         # 검색 결과에서 선택된 정류소 하나를 선택할 수 있게 설정
#         selected_stop = st.selectbox("정류소를 선택하세요:", search_results['정류소명'].unique())
        
#         # 선택한 정류소의 월별 데이터 필터링
#         selected_data = search_results[search_results['정류소명'] == selected_stop]
        
#         # 월별 데이터 추출 및 전처리
#         selected_data['년월'] = pd.to_datetime(selected_data['년월'], format='%y-%b')
#         selected_data = selected_data.sort_values('년월')
        
#         # 그래프 생성
#         plt.figure(figsize=(10, 5))
        
#         # 승차 데이터 추가
#         plt.plot(selected_data['년월'], selected_data['승차'], marker='o', label='승차')
        
#         # 하차 데이터 추가
#         plt.plot(selected_data['년월'], selected_data['하차'], marker='x', label='하차')
        
#         # 그래프 레이아웃 설정
#         plt.title(f"{selected_stop} 정류장의 월별 승차 및 하차 인원")
#         plt.xlabel("월")
#         plt.ylabel("이용자 수")
#         plt.legend()

#         # 그래프를 Streamlit에 표시
#         st.pyplot(plt)
#     else:
#         st.write(f"'{search_query}'에 해당하는 정류소가 없습니다.")
# else:
#     st.write("정류소명을 입력하여 검색하세요.")
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows, Mac, Linux 등 환경에 맞게 설정)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우
# matplotlib.rcParams['font.family'] = 'AppleGothic'  # Mac의 경우
# matplotlib.rcParams['font.family'] = 'NanumGothic'  # Linux 또는 다른 경우

# 한글 지원을 위해 해당 코드 추가
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
@st.cache
def load_data():
    # CSV 파일을 로드 (인코딩 설정 변경)
    monthly_move = pd.read_csv('project/page/대구광역시_시내버스_월별이용자수.csv', encoding='utf-8-sig')
    
    # 따옴표와 쉼표를 제거하고 승차와 하차를 정수로 변환
    monthly_move['승차'] = monthly_move['승차'].str.replace('"', '').str.replace(',', '').astype(int)
    monthly_move['하차'] = monthly_move['하차'].str.replace('"', '').str.replace(',', '').astype(int)
    
    # '년월'을 2020-01, 2020-02 형식으로 변환
    monthly_move['년월'] = monthly_move['년월'].apply(lambda x: '20' + x if len(x) == 5 else x)  # "20-Jan" -> "2020-01"
    monthly_move['년월'] = pd.to_datetime(monthly_move['년월'], format='%Y-%b')  # 년월을 날짜 형식으로 변환

    return monthly_move

# Streamlit 앱 시작
st.title("대구 버스 정류장 데이터 시각화")

# 데이터 로드
df = load_data()

# 사용자에게 정류장 목록 제공
st.subheader("정류장 선택")
bus_stops = df['정류소명'].unique()  # 정류장 이름 목록 생성
choice_list = st.multiselect("보고 싶은 정류장을 선택하세요:", bus_stops)

# 선택된 정류장 데이터 필터링
if choice_list:
    # 선택된 정류장 데이터만 필터링
    filtered_data = df[df['정류소명'].isin(choice_list)]
    
    st.write(f"선택된 정류장 데이터: {', '.join(choice_list)}")
    st.dataframe(filtered_data)

    # Altair를 이용한 시각화
    st.subheader("선택한 정류장의 승차 및 하차 데이터 시각화")

    # Altair 시각화용 데이터 전처리
    filtered_data = filtered_data.sort_values(by=['년월'])
    
    # Altair 차트 생성
    chart = alt.Chart(filtered_data).transform_fold(
        ['승차', '하차'],  # 시각화할 컬럼 선택
        as_=['type', 'value']  # 새롭게 설정할 컬럼 이름
    ).mark_line(point=True).encode(
        x=alt.X('년월:T', title='년월'),  # 날짜를 x축에 맞게 처리
        y=alt.Y('value:Q', title='인원 수'),  # y축은 승차/하차 인원 수
        color='type:N',  # 승차와 하차를 다른 색으로 구분
        tooltip=['년월', 'type', 'value']  # 툴팁에 표시할 항목
    ).properties(
        title="승차 및 하차 인원 추이"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.write("정류장을 선택해주세요.")
