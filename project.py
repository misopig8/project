import streamlit as st
import sqlite3


pages = {
    "회원" : [
        st.Page("./page/signin.py",title="회원가입"),
        st.Page("./page/login.py",title="로그인"),
        st.Page("./page/logout.py",title="로그아웃")
    ],
    "   회원정보":[
        st.Page("./page/addressbring.py",title="내 주소 불러오기"),
        st.Page("./page/addressfix.py",title="내 주소 수정하기")
    ],
    "우리 지역 버스 찾기":[
        st.Page("./page/station.py",title="정거장 별 정보 조회"),
        st.Page("./page/dailymove.py",title="일간 통행량 조회"),
        st.Page("./page/timeline.py",title="시간표/배차 조회")
    ]
}

pg = st.navigation(pages)
pg.run()
