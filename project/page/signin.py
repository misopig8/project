import streamlit as st
import sqlite3

#데이터 베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

    #회원가입 화면
st.title("회원가입")
    #아이디
id = st.text_input("아이디")
    #비밀번호
pw = st.text_input("비밀번호", type='password')
    #비밀번호 확인
pw_check = st.text_input("비밀번호 확인", type='password')
    #이메일
email = st.text_input("이메일")
    #성별(라디오버튼)
gender = st.radio("성별을 선택하세요", ['male','female'])
    #회원가입 버튼
address = st.text_input("주소 - 입력방법 미정")
btn = st.button("회원가입")

    #버튼을 누르면
if btn:
        #비밀번호가 잘 입력되었는지를 확인
    if pw == pw_check:            
            #입력한 정보를 DB에 저장
        sql = f"""
        insert into user(username, password, email, gender)
        values('{id}','{pw}','{email}','{gender}')"""
        cursor.execute(sql)
        conn.commit()
        st.success("회원가입 성공!")
    else:
            #회원가입 실패
            st.error("비밀번호가 일치하지 않습니다.")
    conn.close()