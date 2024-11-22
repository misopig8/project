import streamlit as st
import sqlite3
import pandas as pd

# 데이터 읽기
bus_chart = pd.read_csv('project/page/대구광역시_시내버스 정류소별_노선별_평균배차간격_20231117.csv', encoding='utf-8')

# SQLite DB 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# 로그인 상태를 session_state에 저장
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'station_number' not in st.session_state:
    st.session_state.station_number = None

# 사용자 아이디와 비밀번호 입력
st.title("로그인 및 정류장 번호 수정")
id = st.text_input("아이디를 입력하세요:")
pw = st.text_input("비밀번호를 입력하세요:", type='password')

# 로그인 후 station_number 수정
if st.button("로그인"):
    if id and pw:
        # DB에서 해당 id와 pw로 사용자 찾기
        cursor.execute("SELECT * FROM projectuser WHERE username = ? AND password = ?", (id, pw))
        user = cursor.fetchone()

        if user:
            # 사용자 존재하면 로그인 성공
            st.session_state.logged_in = True
            st.session_state.username = id  # 로그인한 사용자 저장
            st.success(f"환영합니다, {id}님!")
            
            # 새로운 정류장 검색 필드
            station_name = st.text_input('새로운 정류장의 이름을 입력하세요:')
            
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
                    selected_station_display = st.selectbox('검색된 정류장 목록에서 새로운 정류장을 선택하세요:', station_display)

                    # 선택된 정류소의 ID를 추출
                    selected_station_id = station_list[station_list.apply(lambda row: f"{row['정류소ID']} - {row['정류소']}", axis=1) == selected_station_display]['정류소ID'].iloc[0]

                    # 선택된 정류소ID에 해당하는 데이터만 필터링
                    selected_data = filtered_df[filtered_df['정류소ID'] == selected_station_id]
                    st.write(f"### {selected_station_display}의 정류소 아이디")

                    # 새로운 station_number 입력 필드
                    new_station_number = st.text_input("새로운 정류장 번호를 입력하세요:")
                    
                    if new_station_number:
                        # station_number 업데이트
                        cursor.execute("UPDATE projectuser SET station_number = ? WHERE username = ?", (new_station_number, id))
                        conn.commit()  # 변경사항 DB에 반영
                        st.success("정류장 번호가 성공적으로 수정되었습니다.")
                else:
                    st.warning("검색된 정류장이 없습니다.")
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
    else:
        st.error("모든 필드를 입력해주세요.")

# DB 연결 종료
conn.close()
