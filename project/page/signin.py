import streamlit as st
import sqlite3
import pandas as pd

#데이터 베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()


bus_chart = pd.read_csv('project/page/대구광역시_시내버스 정류소별_노선별_평균배차간격_20231117.csv', encoding='utf-8')

#집근처 버스정류장 찾고 그 번호 입력하게 하기

station_name = st.text_input('근처 정류장 이름을 입력하세요:')

if station_name:
    filtered_df = bus_chart[bus_chart['정류소'].str.contains(station_name, na=False)]
    if not filtered_df.empty:
        station_list = filtered_df['정류소'].unique()
    else:
        st.write(f"'{station_name}'에 해당하는 정류장이 없습니다.")





    #회원가입 화면
st.title("회원가입")
    #아이디
id = st.text_input("아이디")
    #비밀번호
pw = st.text_input("비밀번호", type='password')
    #비밀번호 확인
pw_check = st.text_input("비밀번호 확인", type='password')
    #이메일
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