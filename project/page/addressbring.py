import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("내 주소")


# 초기 위치 설정 (위도, 경도)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 서울 시청 위치

# 지도에 마커 추가
folium.Marker([37.5665, 126.9780], popup="서울 시청", tooltip="서울").add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=700, height=500)


from geopy.geocoders import Nominatim

# Geocoding을 위한 geolocator 초기화
geolocator = Nominatim(user_agent="geoapiExercises")

st.title("도로명 주소를 위도 및 경도로 변환")

# 사용자로부터 도로명 주소 5자리 입력받기
address_part = st.text_input("자신의 도로명 주소를 입력하세요")
st.write("예시: 서울특별시 종로구 세종대로 110, 대한민국")

if st.button("위도 및 경도로 변환"):
    # Geocoding을 위해 도로명 주소 부분을 이용
    if address_part:
        try:
            # Nominatim으로 주소 검색
            location = geolocator.geocode(address_part)
            
            if location:
                # 위도, 경도를 화면에 출력
                st.success(f"입력한 주소의 위도: {location.latitude}, 경도: {location.longitude}")
            else:
                st.error("주소를 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.error("도로명 주소를 입력하세요!")
