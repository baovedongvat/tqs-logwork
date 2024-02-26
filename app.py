import streamlit as st
import extra_streamlit_components as stx
import pandas as pd
import numpy as np
from sqlalchemy.sql import text
from htmlTemplates import css, bot_template, user_template
from datetime import date

def storeScore(log_work):
    conn = st.connection("postgresql", type="sql")
    with conn.session as s:
#        log_work = {'username': 'tom', 'result': 0, 'state': "Thục", 'bonus': 1, 'match_id': 1}
        s.execute(
                text('INSERT INTO logwork(username, state, result, bonus, match_id) VALUES (:username, :state, :result, :bonus, :match_id);'),
                params=log_work)
        s.commit()

def main():
    st.title('TQS Logwork')
    cookie_manager = stx.CookieManager()

    c1, c2, c3 = st.columns([1,1,1])

    # Store the initial value of widgets in session state
    if "username" not in st.session_state:
        st.session_state.username = cookie_manager.get('username')
        st.session_state.result = 0
        st.session_state.state = ""
        st.session_state.match_id = 0
        st.session_state.bonus = 0
        
    # Print results.
    st.markdown(
        """
    <style>
    button {
        height: auto;
        padding-top: 50px !important;
        padding-bottom: 50px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    with c1:
        username = st.text_input("Username", cookie_manager.get('username'), key="username")
        if st.button("Register User"):
            cookie_manager.set('username', username, max_age=10 * 365 * 24 * 60 * 60) # Expires 10 year
    with c2:
        st.radio(
            "Choose State 👉",
            key="state",
            index=None,
            options=["Ngụy", "Thục", "Ngô", "Dã Tâm"],
        )
        st.slider('How many bonus points ?', 0, 5, 0, key="bonus")
        option = st.selectbox(
           "Match Index",
           ("0", "1", "2", "3", "4"),
           key="match_id",
           )

    with c3:
        if st.button("LOSE",  use_container_width=True):
            log_work = {'username': st.session_state.username, 'result': 0, 'state': st.session_state.state, 'bonus': st.session_state.bonus, 'match_id': st.session_state.match_id}
            storeScore(log_work)
            st.write(f"{log_work['username']} <{log_work['state']}> at {date.today()} has result : LOSE (bonus {log_work['bonus']})")
        if st.button("WIN",  use_container_width=True):
            log_work = {'username': st.session_state.username, 'result': 1, 'state': st.session_state.state, 'bonus': st.session_state.bonus, 'match_id': st.session_state.match_id}
            storeScore(log_work)
            st.write(f"{log_work['username']} <{log_work['state']}> at {date.today()} has result : WIN (bonus {log_work['bonus']})")

if __name__ == '__main__':
    main()
