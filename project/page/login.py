import streamlit as st
import sqlite3

 #데이터 베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

st.title("로그인")
id = st.text_input("아이디")
pw = st.text_input("비밀번호", type="password")
btn = st.button("로그인")

if btn:        
        #DB에서 (입력한 아이디) 정보를 가져온다
        cursor.execute(f"SELECT * FROM user WHERE username='{id}'")
        row = cursor.fetchone()
        #비밀번호 일치여부 확인
        #userid, username, password ....

        if row:
            db_id = row[1]
            db_pw = row[2]
        else:
            db_id = ''
            db_pw = ''

        if db_pw == pw:
            #로그인을 성공! sidebar ID님 환영합니다.
            st.sidebar.write(f"{id}님 환영합니다.")
        else:            
            #로그인 실패 -> 로그인 실패!
            #ID test
            #PW 123
            st.error("로그인 실패!!")
