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
from streamlit_folium import folium_static
import folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 스타일 설정
plt.rc("font", family="Malgun Gothic")
sns.set(font="Malgun Gothic", rc={"axes.unicode_minus": False}, style='white')

# 제목 표시
st.title("대구시 버스 정류장 및 월별 통행량 정보")

# 데이터 로드
monthly_move = pd.read_csv('project/page/대구광역시_시내버스_월별이용자수.csv', encoding="utf-8")
bus_stops_data = pd.read_csv('project/page/대구광역시_시내버스 정류소 위치정보_20240924.csv', encoding="utf-8")

# 정류장 분포 지도 생성
st.subheader('대구시 내 버스 정류장 분포')
m = folium.Map(location=[35.8714354, 128.601445], tiles='cartodbpositron', zoom_start=12)
for idx, row in bus_stops_data.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['정류소명'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
folium_static(m)

st.line_chart(bus_stops_data)
# 첫 번째 검색창: 대략적인 정보 확인
st.subheader("정류장 대략적인 정보 검색")
search_query_1 = st.text_input("대략적인 정류소 이름을 입력하세요:")

if search_query_1:
    # 검색어를 포함한 정류소 필터링
    search_results = monthly_move[monthly_move['정류소명'].str.contains(search_query_1, case=False, na=False)]
    
    if not search_results.empty:
        st.write(f"'{search_query_1}'에 대한 검색 결과:")
        st.write(search_results[['정류소명', '정류소ID']].drop_duplicates())
    else:
        st.write(f"'{search_query_1}'에 대한 검색 결과가 없습니다.")

# 두 번째 검색창: 정확한 정류소 선택 및 그래프 표시
st.subheader("정확한 정류소 이름 입력")
search_query_2 = st.text_input("정확한 정류소 이름을 입력하세요:")

if search_query_2:
    # 정확한 이름으로 데이터 필터링
    selected_data = monthly_move[monthly_move['정류소명'] == search_query_2]
    
    if not selected_data.empty:
        # '년월' 데이터 전처리
        selected_data['년월'] = pd.to_datetime(selected_data['년월'], format='%Y-%m', errors='coerce')
        selected_data = selected_data.dropna(subset=['년월']).sort_values('년월')
        
        # 승차 및 하차 데이터 그래프 생성
        plt.figure(figsize=(10, 6))
        plt.plot(selected_data['년월'], selected_data['승차'], marker='o', label='승차 인원', color='blue')
        plt.plot(selected_data['년월'], selected_data['하차'], marker='x', label='하차 인원', color='orange')
        
        # 그래프 레이아웃 설정
        plt.title(f"{search_query_2} 정류장의 월별 승차 및 하차 인원")
        plt.xlabel("월")
        plt.ylabel("인원 수")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        
        # Streamlit에 그래프 표시
        st.pyplot(plt)
    else:
        st.write(f"'{search_query_2}'에 대한 데이터가 없습니다.")