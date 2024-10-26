import streamlit as st
import sqlite3

st.title("주소정보 수정")
#데이터 베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()
address = st.text_input("현재 주소 -DB에서 불러오기")
address = st.text_input("바뀔 주소 - 입력방법 미정")
btn = st.button("수정")
