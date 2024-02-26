import streamlit as st
import extra_streamlit_components as stx
import pandas as pd
import numpy as np
from sqlalchemy.sql import text
from htmlTemplates import css, bot_template, user_template

def main():
    conn = st.connection("postgresql", type="sql")
    # Perform query.
    df = conn.query('SELECT * FROM logwork;', ttl="10m")



 #   with conn.session as s:
 #       log_work = {'username': 'tom', 'result': 0, 'state': 1, 'bonus': 1, 'match_id': 1}
 #       s.execute(
 #               text('INSERT INTO logwork(username, state, result) VALUES (:username, :state, :result);'),
 #               params=log_work)
 #       s.commit()
    
    # Print results.
    for row in df.itertuples():
        st.write(f"{row.username} at {row.log_date} has result :{row.result}:")
if __name__ == '__main__':
    main()
