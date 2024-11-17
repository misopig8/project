import streamlit as st
import sqlite3
import pandas as pd

#데이터 베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()


bus_chart = pd.read_csv('project/page/대구광역시_시내버스 정류소별_노선별_평균배차간격_20231117.csv', encoding='utf-8')

#집근처 버스정류장 찾고 그 번호 입력하게 하기




    #회원가입 화면
st.title("회원가입")
    #아이디
id = st.text_input("아이디")
    #비밀번호
pw = st.text_input("비밀번호", type='password')
    #비밀번호 확인
pw_check = st.text_input("비밀번호 확인", type='password')
    #정류장


station_name = st.text_input('근처 정류장 이름을 입력하세요:')

# 사용자 입력을 통해 정류장 이름 검색
station_name = st.text_input('정류장 이름을 입력하세요:')

if station_name:
    # 입력한 정류장 이름에 해당하는 데이터를 필터링
    filtered_df = bus_chart[bus_chart['정류소'].str.contains(station_name, na=False)]

    # 정류장 이름이 있는 경우
    if not filtered_df.empty:
        # 정류소와 정류소ID를 함께 표시할 수 있도록 리스트 준비
        station_list = filtered_df[['정류소ID', '정류소']].drop_duplicates()
        # 정류소ID와 정류소를 결합하여 표시
        station_display = station_list.apply(lambda row: f"{row['정류소ID']} - {row['정류소']}", axis=1)

        # 선택된 정류소를 찾기 위한 selectbox
        selected_station_display = st.selectbox('검색된 정류장 목록에서 선택하세요:', station_display)

        # 선택된 정류소의 ID를 추출
        selected_station_id = station_list[station_list.apply(lambda row: f"{row['정류소ID']} - {row['정류소']}", axis=1) == selected_station_display]['정류소ID'].iloc[0]

        # 선택된 정류소ID에 해당하는 데이터만 필터링
        selected_data = filtered_df[filtered_df['정류소ID'] == selected_station_id]

        st.write(f"### {selected_station_display}의 정류소 아이디")


station_number = st.text_input("정류장 번호")
    #회원가입 버튼
btn = st.button("회원가입")

    #버튼을 누르면
if btn:
        #비밀번호가 잘 입력되었는지를 확인
    if pw == pw_check:            
            #입력한 정보를 DB에 저장
        sql = f"""
        insert into user(username, password, station_number)
        values('{id}','{pw}','{station_number}',)"""
        cursor.execute(sql)
        conn.commit()
        st.success("회원가입 성공!")
    else:
            #회원가입 실패
            st.error("비밀번호가 일치하지 않습니다.")
    conn.close()